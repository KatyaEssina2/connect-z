from connectz import *
import unittest
import subprocess

WIDTH = 3
HEIGHT = 3
STREAK = 3


class TestDraw(unittest.TestCase):
    """Test draw win RETURN 0"""
    def test_draw(self):
        """Verify that a full grid with no winning streak returns a draw"""
        game_moves = [1, 2, 3, 1, 3, 2, 1, 3, 2]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 0)

    def test_big_draw(self):
        """Verify that a draw can be achieved for a large grid by creating a grid
        full of alternating half rows of a player counter"""
        # create a draw
        game_moves = []
        height = 20
        width = 10000
        win_streak = 10000

        for y in range(height):
            if y % 2 == 0:
                player_1_offset = 0
                player_2_offset = width/2
            else:
                player_1_offset = width/2
                player_2_offset = 0
            for x in range(1, int(width/2) + 1):
                game_moves.append(int(x + player_1_offset))
                game_moves.append(int(x + player_2_offset))
        result = play_connectz(game_moves, width, height, win_streak)
        self.assertEqual(result, 0)


class TestPlayer1Win(unittest.TestCase):
    """Test player 1 win RETURN 1"""
    def test_p1_win_diagonal_edge(self):
        """Verify that Player 1 can win the game on a diagonal where the
         last counter entered is at the end of the streak"""
        game_moves = [1, 2, 2, 3, 1, 3, 3]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 1)

    def test_p1_win_diagonal_mid(self):
        """Verify that Player 1 can win the game on a diagonal where the
         last counter entered is in the middle of the streak"""
        game_moves = [1, 2, 3, 3, 3, 1, 2]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 1)

    def test_p1_win_vertical(self):
        """Verify that Player 1 can win the game on a vertical streak"""
        game_moves = [1, 2, 1, 2, 1]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 1)

    def test_big_p1_win_vertical(self):
        """Verify that Player 1 can win the game on a vertical streak for a large grid"""
        # create a draw
        game_moves = []
        height = 10000
        width = 2
        win_streak = 10000

        for y in range(height):
            for i in range(1, 3):
                game_moves.append(i)
        # remove the last element to make a valid game
        result = play_connectz(game_moves[:-1], width, height, win_streak)
        self.assertEqual(result, 1)

    def test_big_p1_win_horizontal(self):
        """Verify that Player 1 can win the game on a horizontal streak for a large grid"""
        # create a draw
        game_moves = []
        height = 2
        width = 10000
        win_streak = 10000

        for x in range(1, width + 1):
            game_moves.extend([x, x])
        # remove the last element to make a valid game
        result = play_connectz(game_moves[:-1], width, height, win_streak)
        self.assertEqual(result, 1)


class TestPlayer2Win(unittest.TestCase):
    """Test player 2 win RETURN 2"""
    def test_p2_win_horizontal_edge(self):
        """Verify that Player 2 can win the game on a horizontal streak where the
         last counter entered is at the end of the streak"""
        game_moves = [1, 2, 3, 1, 1, 2, 2, 3]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 2)

    def test_p2_win_horizontal_mid(self):
        """Verify that Player 2 can win the game on a horizontal streak where the
         last counter entered is in the middle of the streak"""
        game_moves = [1, 2, 3, 1, 1, 3, 3, 2]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 2)

    def test_p2_win_anticlock_diagonal(self):
        """Verify that Player 2 can win the game on an anti clockwise diagonal streak"""
        game_moves = [1, 2, 1, 3, 3, 1, 3, 2]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 2)


class TestIncompleteGame(unittest.TestCase):
    """Test incomplete game RETURN 3"""
    def test_incomplete_basic(self):
        """Verify that a no win game, where the grid is not full results in an incomplete game"""
        game_moves = [1, 2, 3, 1]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 3)

    def test_incomplete_no_moves(self):
        """Verify that a game with no moves results in an incomplete game"""
        game_moves = []
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 3)


class TestIllegalContinue(unittest.TestCase):
    """Test illegal continue RETURN 4"""
    def test_illegal_continue_p1_win(self):
        """Verify that once Player 1 wins, a move by Player 2 results in an illegal continue"""
        game_moves = [1, 2, 1, 2, 1, 3]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 4)

    def test_illegal_continue_p2_win(self):
        """Verify that once Player 2 wins, a move by Player 1 results in an illegal continue"""
        game_moves = [1, 2, 3, 1, 1, 3, 3, 2, 2]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 4)


class TestIllegalRow(unittest.TestCase):
    """Test illegal row (overflow) RETURN 5"""
    def test_illegal_first_row(self):
        """Verify that if the number of moves into the first column exceeds the height of the grid
        the game results in an illegal row"""
        game_moves = [1, 1, 1, 1, 1]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 5)

    def test_illegal_last_row(self):
        """Verify that if the number of moves into the last column exceeds the height of the grid
        the game results in an illegal row"""
        game_moves = [3, 3, 3, 3, 3, 3, 3, 3]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 5)


class TestIllegalColumn(unittest.TestCase):
    """Test for illegal column RETURN 6"""
    def test_illegal_column_zero(self):
        """Verify that attempting to add a counter to column 0 is impossible and results in an illegal column"""
        game_moves = [0, 2, 3, 1]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 6)

    def test_illegal_column_out_of_range(self):
        """Verify that attempting to add a counter to a column which is greater than the width of the grid
        results in an illegal column"""
        game_moves = [1, 2, 13, 1]
        result = play_connectz(game_moves, WIDTH, HEIGHT, STREAK)
        self.assertEqual(result, 6)


class TestIllegalGame(unittest.TestCase):
    """Test for illegal game RETURN 7"""
    def test_illegal_game_too_short(self):
        """Verify that specifying a win streak that is greater than the height (and width) of the grid results
        in an illegal game"""
        result = play_connectz([], 5, 4, 6)
        self.assertEqual(result, 7)

    def test_illegal_game_too_narrow(self):
        """Verify that specifying a win streak that is greater than the width (and height) of the grid results
        in an illegal game"""
        result = play_connectz([], 4, 5, 6)
        self.assertEqual(result, 7)

    def test_illegal_game_draw(self):
        """Verify specifying a grid that is impossible to win, even if the moves COULD result in a draw, result in
        an illegal game"""
        game_moves = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
        result = play_connectz(game_moves, 5, 3, 6)
        self.assertEqual(result, 7)


class TestInputs(unittest.TestCase):
    """
    Test file inputs that should cause errors
    """
    # bad file data RETURN 8
    def test_empty_file(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/empty_file.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(8))

    def test_non_ascii_first_row(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/non_ascii_first_row.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(8))

    def test_non_numeric_first(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/non_numeric_first.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(8))

    def test_not_enough_dims(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/not_enough_dims.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(8))

    def test_non_numeric_middle(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/non_numeric_middle.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(8))

    def test_non_ascii_middle(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/non_ascii_middle_row.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(8))

    # cant open file RETURN 9
    def test_wrong_file_path(self):
        result = subprocess.run(['python', 'connectz.py', './test_cases/this_file_doesnt_exist.txt'], capture_output=True)
        self.assertEqual(result.stdout.decode('ascii'), format_output(9))

    # not the right number of arguments given
    def test_cli_args_none(self):
        result = subprocess.run(['python', 'connectz.py'], capture_output=True)
        self.assertEqual(result.stderr.decode('ascii'), format_output('connectz.py: Provide one input file'))

    def test_cli_args_too_many(self):
        result = subprocess.run(['python', 'connectz.py', './test_casess/draw.txt', './test_cases/player_2.txt'], capture_output=True)
        self.assertEqual(result.stderr.decode('ascii'), format_output('connectz.py: Provide one input file'))


if __name__ == '__main__':
    unittest.main()
