import sys
from functools import lru_cache

DIRECTIONS = ['horizontal', 'vertical', 'diagonal_clockwise', 'diagonal_anticlockwise']


class Column:
    def __init__(self, index):
        self.counters = []
        self.index = index

    def __str__(self):
        return f'Column {self.index}'


class Counter:
    def __init__(self, player_no, column):
        self.player_no = player_no
        self.horizontal = []
        self.vertical = []
        self.diagonal_clockwise = []
        self.diagonal_anticlockwise = []

    def __str__(self):
        return f'Player {self.player_no} counter'


class Grid:
    def __init__(self, width, height, win_streak):
        self.width = int(width)
        self.height = int(height)
        self.win_streak = int(win_streak)
        self.columns = {}
        # initialise game as incomplete
        self.result = 3

    def __str__(self):
        return f'Grid ({self.width}x{self.height}) win streak required: {self.win_streak}'

    @staticmethod
    def set_surrounding_relationships(column, neighbour_column, counter):
        """
        Update surrounding Counter node spatial relationships to include added counter.
        :param column: an instance of Column to which a counter was added
        :param neighbour_column: an instance of Column to the left or right of column where counter was added
        :param counter: added instance of Counter
        """
        added_index = len(column.counters) - 1
        direction_index_mapping = {'horizontal': added_index,
                                   'diagonal_clockwise': added_index + 1 if column.index < neighbour_column.index else added_index - 1,
                                   'diagonal_anticlockwise': added_index - 1 if column.index < neighbour_column.index else added_index + 1}

        for direction, index in direction_index_mapping.items():
            if len(neighbour_column.counters) > index > -1:
                neighbour_counter = neighbour_column.counters[index]
                # update adjacent node (based on direction) as well as the added node
                getattr(neighbour_counter, direction).append(counter)
                getattr(counter, direction).append(neighbour_counter)

    def add_counter(self, counter, column_number):
        """
        Add Counter to correct position in Grid
        :param counter: added instance of Counter
        :param column_number: column number to which counter should be added to in grid
        """
        if column_number not in self.columns:
            # only create column space as we need it
            self.columns[column_number] = Column(column_number)

        self.result = self.validate_move(column_number)
        if self.result == 3:
            column = self.columns[column_number]
            column.counters.append(counter)

            # set vertical relationships between new counter and existing counters
            if len(column.counters) > 1:
                counter.vertical.append(column.counters[-2])
                column.counters[-2].vertical.append(counter)

            # horizontal& diagonal relationships
            if column_number > 1 and column_number - 1 in self.columns:
                prev_column = self.columns[column_number - 1]
                self.set_surrounding_relationships(column, prev_column, counter)

            if column_number < self.width and column_number + 1 in self.columns:
                next_column = self.columns[column_number + 1]
                self.set_surrounding_relationships(column, next_column, counter)

            self.result = self.check_winning_streak(counter)

    def check_winning_streak(self, counter):
        """
        Starting at added counter check if a winning streak has been achieved in any direction
        :param counter: added instance of Counter
        :return: if the game has been won or lost
        """
        for direction in DIRECTIONS:
            streak = count_direction_streak(counter, direction, counter)
            if streak >= self.win_streak:
                return counter.player_no
        # no one has won
        if self.is_full():
            return 0
        return 3

    def validate_move(self, column_number):
        """
        :param column_number: column to which we want to add a counter
        :return: an error status if columns/rows are full or an 'incomplete' status
        """
        if not 1 <= column_number <= self.width:
            # illegal column
            return 6
        elif len(self.columns[column_number].counters) == self.height:
            # illegal row
            return 5
        elif self.result == 1 or self.result == 2:
            return 4
        return 3

    def is_full(self):
        """
        :return: if the grid is full or not
        """
        for column_number in self.columns:
            if len(self.columns[column_number].counters) != self.height:
                return False
        return True


@lru_cache(maxsize=None)
def count_direction_streak(current_counter, direction, prev_counter, streak=1):
    """
    Loop and recurse to count streak
    :param current_counter: an instance of Counter who's adjacent nodes we are searching
    :param direction: direction of search
    :param prev_counter: prior instance of Counter
    :param streak: current streak
    :return: streak
    """
    if not getattr(current_counter, direction):
        return 1
    for adjacent_counter in getattr(current_counter, direction):
        if adjacent_counter != prev_counter and adjacent_counter.player_no == current_counter.player_no:
            streak = count_direction_streak(adjacent_counter, direction, current_counter, streak) + 1
    return streak


def is_valid_game(width, height, win_streak):
    """
    Check if the parameters specified in the game will result in a winnable game
    :return: validity of game
    """
    return win_streak <= width or win_streak <= height


def play_connectz(game_moves, width, height, win_streak):
    if is_valid_game(width, height, win_streak):
        grid = Grid(width, height, win_streak)
        player = 1
        # loop over rows one by one to avoid loading into memory
        for move in game_moves:
            if not valid_line(move):
                return 8
            column_number = int(str(move).strip())
            grid.add_counter(Counter(player, column_number), column_number)

            if 4 <= grid.result <= 8:
                # game has reached an end point
                break

            # update player
            player = 1 if player == 2 else 2

        return grid.result
    return 7


def is_ascii(string):
    try:
        string.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def format_output(result):
    return f'{str(result)}\n'


def valid_line(line):
    line = str(line).strip()
    if line and is_ascii(line) and all(c.isdigit() for c in line if c != ' '):
        return True
    return False


def main():
    if len(sys.argv) != 2:
        sys.exit('connectz.py: Provide one input file')
    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as i:
            meta_data_str = i.readline()
            if not valid_line(meta_data_str):
                # if file is blank or non ASCII
                sys.stdout.write(format_output(8))
            else:
                meta_data = meta_data_str.strip().split(' ')
                if len(meta_data) < 3:
                    sys.stdout.write(format_output(8))
                result = play_connectz(i, meta_data[0], meta_data[1], meta_data[2])
                sys.stdout.write(format_output(result))
                count_direction_streak.cache_clear()
    except EnvironmentError:
        # cant open file
        sys.stdout.write(format_output(9))

    sys.exit()


if __name__ == '__main__':
    main()
