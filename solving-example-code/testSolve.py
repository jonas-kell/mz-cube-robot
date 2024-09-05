import twophase.solver as sv

# https://github.com/hkociemba/RubiksCube-TwophaseSolver

# CAUTION: first run generates tables in the folder twopahse
# Depending on the hardware, this may take up to an hour, so be sure to run on time beforehand

cubestring = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"

sol = sv.solve(cubestring, 19, 2)

print(sol)
