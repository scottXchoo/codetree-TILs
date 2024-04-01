"""
[2차시도] 09:10 ~
NxN 좌상단 (1, 1)
rudolf_move
- 가장 가까운 산타 찾기 (탈락 X)
- 2명 이상이면, r좌표가 큰 산타 => c좌표가 큰 산타
- 그 산타를 향해 가장 가까워지는 방향으로 8방향으로 돌진
santa_move
- 1~P번까지 움직임 (기절했거나 이미 게임에서 탈락한 산타는 X)
- 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동
- 다른 산타가 있거나 밖으로는 이동 X
- 움직일 수 있는 칸이 없다면, 이동 X
- '상우하좌' 순서로 4방향 중 한 곳으로 움직일 수 있음
conflict
- 루돌프 => 산타 : 해당 산타 +C점 / 산타는 루돌프가 이동해온 방향으로 C만큼 밀려남
- 산타 => 루돌프 : 해당 산타 +D점 / 산타는 자신이 이동해온 반대 방향으로 D만큼 밀려남
- 산타가 밀려났을 때, 밖이면 탈락! & 산타가 있다면 상호작용!
interaction
- 산타(1)와 산타(2)가 만나게 되면 산타(2)가 그 방향으로 1칸 밀림
- 산타(2)가 산타(3)을 밀게 되면, 산타(3)도 그 방향으로 1칸 밀림
- 당연히 밖으로 나가게 되면 게임에서 탈락
sturn
- k번째 턴에 기절되면, k+1번째 턴까지 기절, k+2번째 턴부터 다시 정상
- 기절한 산타를 돌진 대상으로 선택할 수 있음
distance : 거리를 구하는 유틸함수
"""

N, M, P, C, D = map(int, input().split())
rr, rc = map(int, input().split())
board = [[0] * (N + 1) for _ in range(N + 1)]
santa_info = [0 for _ in range(P + 1)]
for _ in range(P):
    idx, r, c = map(int, input().split())
    santa_info[idx] = [r, c, True, 0, 0]  # r, c, 생존 여부, 스턴, 점수
    board[r][c] = idx
inf = float("inf")


def dist(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


def is_in_range(r, c):
    return 1 <= r <= N and 1 <= c <= N


def rudolf_move(c_rr, c_rc):
    # print("rudolf_move")
    santa_dist = []
    for santa in range(1, P + 1):
        sr, sc, is_alive, _, _ = santa_info[santa]
        if is_alive:
            distance = dist(c_rr, c_rc, sr, sc)
            santa_dist.append([santa, distance, sr, sc])
    santa_dist.sort(key=lambda x: (x[1], -x[2], -x[3]))
    _, _, sel_santa_r, sel_santa_c = santa_dist[0]

    n_rr, n_rc = c_rr, c_rc
    n_dr, n_dc = 0, 0
    min_dist = inf
    for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        distance = dist(c_rr + dr, c_rc + dc, sel_santa_r, sel_santa_c)
        if min_dist > distance:
            min_dist = distance
            n_rr, n_rc = c_rr + dr, c_rc + dc
            n_dr, n_dc = dr, dc
    return n_rr, n_rc, n_dr, n_dc


def interaction(n_r, n_c, dr, dc, santa):
    # print("산타와 산타가 부딪침")
    selected_santa = santa
    move_r, move_c = n_r, n_c
    while True:
        # print("move_r, move_c", move_r, move_c)
        # print("selected_santa", selected_santa)
        if not is_in_range(move_r, move_c):
            break
        if board[move_r][move_c] != 0: # 산타가 있다면
            # print("board[move_r][move_c]", board[move_r][move_c])
            prev_santa = board[move_r][move_c]
            # print("prev_santa", prev_santa)
            board[move_r][move_c] = selected_santa
            r, c, is_alive, sturn, score = santa_info[selected_santa]
            santa_info[selected_santa] = move_r, move_c, is_alive, sturn, score
            selected_santa = prev_santa
            move_r += dr
            move_c += dc
        else: # 산타가 없다면
            board[move_r][move_c] = selected_santa
            r, c, is_alive, sturn, score = santa_info[selected_santa]
            santa_info[selected_santa] = move_r, move_c, is_alive, sturn, score
            break


def conflict(nr, nc, dr, dc, is_santa):
    global rr, rc
    if is_santa:
        # print("산타 => 루돌프")
        if nr == rr and nc == rc:
            # print("산타와 루돌프 충돌!")
            santa = is_santa
            sr, sc, is_alive, sturn, score = santa_info[santa]
            n_sr, n_sc = sr - dr * D, sc - dc * D
            sturn = c_m + 1
            score += D
            if not is_in_range(n_sr, n_sc):
                is_alive = False
            santa_info[santa] = n_sr, n_sc, is_alive, sturn, score
            board[nr][nc] = 0
            # print("santa_info[santa]", santa_info[santa])
            # print("board", board)
            interaction(n_sr, n_sc, -dr, -dc, santa)
    else:
        # print("루돌프 => 산타")
        if board[nr][nc] != 0:
            # print("산타와 충돌!")
            rr, rc = nr, nc
            santa = board[nr][nc]
            sr, sc, is_alive, sturn, score = santa_info[santa]
            n_sr, n_sc = sr + dr * C, sc + dc * C
            sturn = c_m + 1
            score += C
            if not is_in_range(n_sr, n_sc):
                is_alive = False
            santa_info[santa] = n_sr, n_sc, is_alive, sturn, score
            board[nr][nc] = 0
            # print("santa_info[santa]", santa_info[santa])
            # print("board", board)
            interaction(n_sr, n_sc, dr, dc, santa)
        else:
            # print("산타 X")
            rr, rc = nr, nc


def santa_move(sr, sc):
    # print("santa_move")
    n_sr, n_sc = sr, sc
    n_dr, n_dc = 0, 0
    min_dist = dist(sr, sc, rr, rc)
    for dr, dc in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        tmp_r, tmp_c = sr + dr, sc + dc
        if not is_in_range(tmp_r, tmp_c) or board[tmp_r][tmp_c] != 0:
            continue
        distance = dist(tmp_r, tmp_c, rr, rc)
        if min_dist > distance:
            min_dist = distance
            n_sr, n_sc = tmp_r, tmp_c
            n_dr, n_dc = dr, dc
    return n_sr, n_sc, n_dr, n_dc

c_m = 1
while c_m <= M:
    # print()
    # print("-----", c_m)
    # rudolf_move
    n_rr, n_rc, n_dr, n_dc = rudolf_move(rr, rc)
    conflict(n_rr, n_rc, n_dr, n_dc, 0)
    # print("현재 루돌프 위치: ", rr, rc)

    # santa_move
    for santa in range(1, P + 1):
        sr, sc, is_alive, sturn, score = santa_info[santa]
        if not is_alive or c_m <= sturn:
            continue
        n_sr, n_sc, n_dr, n_dc = santa_move(sr, sc)
        santa_info[santa] = n_sr, n_sc, is_alive, sturn, score
        board[sr][sc] = 0
        board[n_sr][n_sc] = santa
        conflict(n_sr, n_sc, n_dr, n_dc, santa)

    # 전체 점수 획득
    fail_santa = 0
    for santa in range(1, P + 1):
        sr, sc, is_alive, sturn, score = santa_info[santa]
        if not is_alive:
            fail_santa += 1
            continue
        santa_info[santa] = sr, sc, is_alive, sturn, score + 1

    if fail_santa == P:
        break
    # print("santa_info", santa_info)
    c_m += 1

answer = []
for idx in range(1, P + 1):
    _, _, _, _, score = santa_info[idx]
    answer.append(score)
print(*answer)