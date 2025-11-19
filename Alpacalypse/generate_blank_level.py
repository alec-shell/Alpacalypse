"""
make_level.py: Blank level generator.
"""

with open('levels/lvl_09.txt', 'w') as f:
    f.write("backdrop = Dark_Forest_Background.jpg\n")
    for i in range(20):
        for j in range(27):
            if j == 26:
                f.write("00")
            else:
                f.write("00,")
        f.write('\n')
