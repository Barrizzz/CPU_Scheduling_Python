from scheduler import Process

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
    3: [
      Process("P1", 4, 5, 2),
      Process("P2", 2, 3, 1),
      Process("P3", 2, 8, 4),
      Process("P4", 3, 6, 3)
    ]
}