import twophase.solver as sv

# https://github.com/hkociemba/RubiksCube-TwophaseSolver

cubestring = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"

sol = sv.solve(cubestring, 19, 2)

print(sol)
