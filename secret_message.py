import hashlib as _hashlib
import binascii as _binascii
import threading
from collections import deque
def _isha(m):
    h = ''
    for i in xrange(1048576):
        h = _hashlib.sha256(h + m).digest()
    return h

def _mrc4(key, data):
    S = range(256)
    j = 0
    for i in xrange(256):
        j += S[i] + ord(key[i % len(key)])
        S[i], S[j & 255] = S[j & 255], S[i]
    i = 0
    j = 0
    out = ''
    for b in data:
        for x in xrange(1021):
            i = i + 1 & 255
            j = j + S[i] & 255
            S[i], S[j] = S[j], S[i]
        K = S[S[i] + S[j] & 255]
        out += chr(ord(b) ^ K)
    return out

class Robot(object):
    def __init__(self):
        self.__pos = (0, 0)
        self.__stk = ''

    def moveDown(self):
        return self.move('d')

    def moveLeft(self):
        return self.move('l')

    def moveRight(self):
        return self.move('r')

    def moveUp(self):
        return self.move('u')

    def move(self, d):
        if type(d) != str or len(d) != 1 or d not in 'dlru':
            raise ValueError()
        x, y = self.__pos
        dx, dy = {'d': (0, 1), 'l': (-1, 0), 'r': (1, 0), 'u': (0, -1)}[d]
        if not (0 <= x + dx < 32 and 0 <= y + dy < 32):
            return False
        cx = x if d != 'l' else x + dx
        cy = y if d != 'u' else y + dy
        if 1 << cx * 64 + (d in 'du') * 32 + cy & 26844546157757908605186262229192653878578790248409047522240381718974817992673833533202662261529304322744224532008175637875960981945428742173638190354788235892440952732995510455203924178576193207418500972553190155627910745959635098145735353156664378707085134514905353234797611910783409289555480200477115926243020733701292643901922536275633771162354785575544824260162252352633148807109248458792917829360718053384803485822028837181334828912816481025393310241630256069695764830281698998184918254942780357287385514160554802605448394817117940470877383879937162226135532298929876967998455401393902995434413439939832660140492L:
            return False
        self.__stk += d
        self.__pos = (x + dx, y + dy)
        for bt in ('ud', 'du', 'lr', 'rl'):
            self.__stk = self.__stk.replace(bt, '')
        return True

    def solve(self):
        x, y = self.__pos
        if self.__pos != (31, 31):
            return 'You are still %d left and %d above where you should be!' % (31 - x, 31 - y)
        k = _isha(self.__stk)
        if not k.endswith(b'\x04\x85'):
            return 'Cheater! Go solve it correctly!'
        return _mrc4(k[:-3], _binascii.a2b_base64('QfvfXYn4NTzBGO8yj9r0NN94zFzTJas12P2/jMTsd3PQe62HyXtYvHhlk1qdltxJxigAqwZ3s9j+a8thAeYi3n6Mf7D58x+Dg8CXI/KQRG0zPhraYzLdg4bvMZIa9xc='))

from collections import deque

class RobotSolver:
    def __init__(self):
        self.robot = Robot()

    def solve_maze(self):
        """
        This uses a BFS(Breadth-First Search) algorithm to solve the maze. It tries all possible moves and keeps track of visited positions.
        """
        queue = deque([(self.robot._Robot__pos, '')])
        visited = set()
        while queue:
            (x, y), path = queue.popleft()
            self.robot._Robot__pos = (x, y)
            self.robot._Robot__stk = path

            result = self.robot.solve()
            if result.startswith('You are still'):
                if (x, y) in visited:
                    continue
                visited.add((x, y))
                left, above = self.parse_position(result)

                # Try all possible moves
                if self.robot.move('r'):  # Move Right
                    queue.append(((x + 1, y), path + 'r'))
                    self.robot.move('l')  # Move back
                if self.robot.move('l'):  # Move Left
                    queue.append(((x - 1, y), path + 'l'))
                    self.robot.move('r')  # Move back
                if self.robot.move('d'):  # Move Down
                    queue.append(((x, y + 1), path + 'd'))
                    self.robot.move('u') # Move back
                if self.robot.move('u'):  # Move Up
                    queue.append(((x, y - 1), path + 'u'))
                    self.robot.move('d')  # Move back
            elif result.startswith('Cheater'):
                raise Exception("Invalid solution. Please try a different approach.")
            else:
                return result

    def parse_position(self, result):
        parts = result.split()
        left = int(parts[3])
        above = int(parts[6])
        return left, above

solver = RobotSolver()
solution = solver.solve_maze()
print solution

        




