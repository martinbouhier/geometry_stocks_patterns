import matplotlib.pyplot as plt

# Head and showlders
Q1 = (2, 20)
Q2 = (4, 25)
Q3 = (6, 20)
P1 = (1, 5)
P2 = (3, 5)
P3 = (5, 5)
P4 = (7, 5)

O_ = (
    (P3[0] - P2[0]) / 2 + (P2[0]),
    (P3[1])
)
OQ2 = (Q2[0] - O_[0], Q2[1] - O_[1])
OP3 = (P3[0] - O_[0], P3[1] - O_[1])


X = [P1[0], Q1[0], P2[0], Q2[0], P3[0], Q3[0], P4[0]]
Y = [P1[1], Q1[1], P2[1], Q2[1], P3[1], Q3[1], P4[1]]


plt.plot(X, Y, marker='o')
plt.plot([O_[0], Q2[0]], [O_[1], Q2[1]], linestyle='--', color='black')
plt.plot([O_[0], P3[0]], [O_[1], P3[1]], linestyle='--', color='black')


coordinates = [
    ('P1', P1[0], P1[1]),
    ('Q1', Q1[0], Q1[1]),
    ('P2', P2[0], P2[1]),
    ('Q2', Q2[0], Q2[1]),
    ('P3', P3[0], P3[1]),
    ('Q3', Q3[0], Q3[1]),
    ('P4', P4[0], P4[1]),
    ('O', O_[0], O_[1])
]
for x in coordinates:
    plt.annotate(x[0], (x[1], x[2]))

plt.show()
