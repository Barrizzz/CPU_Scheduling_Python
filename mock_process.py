from process import Process

processes = {
    # No priority
    1: [
      Process("P1", 0, 5, 0),
      Process("P2", 2, 3, 0),
      Process("P3", 2, 8, 0),
      Process("P4", 6, 6, 0)
    ],
    # With priority
    2: [
      Process("P1", 0, 4, 4),
      Process("P2", 1, 3, 3),
      Process("P3", 2, 5, 2),
      Process("P4", 3, 2, 1)
    ],
    # SJF and Priority same
    3: [
      Process("P1", 1, 30, 4),
      Process("P2", 1, 2, 1),
      Process("P3", 1, 3, 2),
      Process("P4", 1, 4, 3)
    ],
    # SJF is way better than priority
    4: [
      Process("P1", 1, 30, 1),
      Process("P2", 1, 2, 4),
      Process("P3", 1, 3, 3),
      Process("P4", 1, 4, 2)
    ],
    # Round Robin is best
    5: [
      Process("P1", 0, 30, 4),
      Process("P2", 1, 2, 1),
      Process("P3", 1, 2, 2),
      Process("P4", 1, 2, 3)
    ]
}