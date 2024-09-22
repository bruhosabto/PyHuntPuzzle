import sys
import termios
import tty

class CursorTerminal:
	def __init__(self):
		None
	def get_cursor_position(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			sys.stdout.write("\033[6n")
			sys.stdout.flush()

			response = ""
			while True:
				ch = sys.stdin.read(1)
				response += ch
				if ch == "R":
					break
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

		response = response.lstrip("\033[")
		rows, cols = map(int, response[:-1].split(";"))
		return rows
		
	def getLinha(self):
		return self.get_cursor_position()
