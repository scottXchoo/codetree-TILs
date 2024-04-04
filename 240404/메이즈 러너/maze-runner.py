import copy

# 입력 상태 : 15분 소요 (이거 반성) (19:15)
N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

cand_info = [[] for _ in range(M)]
cand_set = {}
for i in range(M):
    r, c = map(int, input().split())
    cand_info[i] = [False, [r-1, c-1]]
    cand_set[i] = (r-1, c-1)

inf = float("inf")
exit_r, exit_c = map(int, input().split())
exit_r -= 1
exit_c -= 1
total_dist = 0


def is_in_range(row, col):
    return 0 <= row < N and 0 <= col < N


def distance(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)


def move(cand_r, cand_c, index):
    global total_dist, exit_r, exit_c
    cur_dist = distance(exit_r, exit_c, cand_r, cand_c)
    min_dist = cur_dist
    next_r, next_c = cand_r, cand_c
    for dr, dc in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
        nr, nc = cand_r + dr, cand_c + dc
        if not is_in_range(nr, nc) or board[nr][nc] != 0:
            continue
        next_dist = distance(exit_r, exit_c, nr, nc)
        if min_dist > next_dist:
            min_dist = next_dist
            cand_set[index] = (nr, nc)
            next_r, next_c = nr, nc
    # 움직인 거리를 total_dist에 추가
    total_dist += distance(cand_r, cand_c, next_r, next_c)
    # 탈출했다면, True로 변경
    if (next_r == exit_r) and (next_c == exit_c):
        del cand_set[index]


def find_cand():
    min_dist = inf
    temp = []
    for c_r, c_c in cand_set.values():
        temp.append([c_r, c_c])
    temp.sort(key=lambda x: (x[0], x[1]))
    nr, nc = 0, 0
    for cand_r, cand_c in temp:
        dist = distance(exit_r, exit_c, cand_r, cand_c)
        if min_dist > dist:
            min_dist = dist
            nr, nc = cand_r, cand_c
    return nr, nc


def rectangle():
    global exit_r, exit_c
    nr, nc = find_cand()
    h, w = abs(exit_r - nr) + 1, abs(exit_c - nc) + 1
    length = max(h, w)
    p_r, p_c = min(exit_r, nr), min(exit_c, nc)
    if length > w:
        diff_c = length - w
        while diff_c > 0 and p_c > 0:
            p_c -= 1
            diff_c -= 1
    else:
        diff_r = length - h
        while diff_r > 0 and p_r > 0:
            p_r -= 1
            diff_r -= 1
    return p_r, p_c, length


def rotation(p_r, p_c, length):
    global exit_r, exit_c
    temp = copy.deepcopy(board)
    temp_cand = []
    temp_exit_r, temp_exit_c = 0, 0
    for i in range(p_r, p_r + length):
        for j in range(p_c, p_c + length):
            if temp[i][j]:
                temp[i][j] -= 1

    for i in range(p_r, p_r + length):
        for j in range(p_c, p_c + length):
            # (p_r, p_c)를 (0, 0)으로 옮기기
            o_i, o_j = i - p_r, j - p_c
            # 변환된 상태에서 회전
            r_i, r_j = o_j, length - o_i - 1
            # 다시 (p_r, p_c) 더하기
            n_i, n_j = r_i + p_r, r_j + p_c
            board[n_i][n_j] = temp[i][j]
            # 참가자 회전
            for key in cand_set:
                if (i, j) == cand_set[key]:
                    temp_cand.append([key, n_i, n_j])
            # 탈출구 회전
            if i == exit_r and j == exit_c:
                temp_exit_r, temp_exit_c = n_i, n_j
    # 참가자 값 적용
    for key, t_i, t_j in temp_cand:
        cand_set[key] = (t_i, t_j)
    # 탈출구 값 적용
    exit_r, exit_c = temp_exit_r, temp_exit_c


c_time = 0
while c_time < K:
    # move() : 각 참가자들 이동
    for idx in range(M):
        if idx in cand_set:
            r, c = cand_set[idx]
            move(r, c, idx)

    # rectangle() : 가장 작은 정사각형 구하기
    point_r, point_c, length = rectangle()

    # rotation() : 정사각형을 시계방향으로 90도 회전
    rotation(point_r, point_c, length)

    # 모든 참가자들 탈출 시, break
    if len(cand_set) == 0:
        break
    c_time += 1

# 정답 제출
print(total_dist)
print(*[exit_r+1, exit_c+1])