_remains = 0

def _construct_sudoku(sudoku):
    ret = []
    for i in range(9):
        ret.append([])
        for j in range(9):
            ret[i].append([sudoku[i][j]]+[0]*9)
    return ret

def _deconstruct_sudoku(sudoku):
	ret=[]
	for i in range(9):
		ret.append([])
		ret[i]=[sudoku[i][j][0] for j in range(9)]
	return ret

def _check_candidacy(sud,r,c,cand):
	flag = True
	if cand in [sud[r][x][0] for x in range(9)]:
		flag = False
	if cand in [sud[x][c][0] for x in range(9)]:
		flag = False
	box = []
	for x in range(r-(r%3),r-(r%3)+3):
		for y in range(c-(c%3),c-(c%3)+3):
			if sud[x][y][0]:
				box += [sud[x][y][0]]
	if cand in box:
		flag = False
	return flag

def _pencil(sud):
	for rowindex,row in enumerate(sud):
		for columnindex,cell_list in enumerate(row):
			if cell_list[0] == 0:
				for cand in range(1,10):
					if _check_candidacy(sud,rowindex,columnindex,cand):
						sud[rowindex][columnindex][cand] = 1
					else:
						sud[rowindex][columnindex][cand] = 0
			else:
				cell_list = [cell_list[0]] + [0]*9
					
def _clear_pencils_after_write(sud,i,j,cand):
	sud[i][j][cand] = 0
	for x in range(9):
		sud[i][x][cand] = 0
	for y in range(9):
		sud[y][j][cand] = 0
	for x in range(i-(i%3),i-(i%3)+3):
		for y in range(j-(j%3),j-(j%3)+3):
			sud[x][y][cand] = 0

def _pen(sud):
	global _remains
	for rowindex,row in enumerate(sud):
		for colindex,cell_list in enumerate(row):
			if cell_list[0] == 0 and cell_list.count(1) == 1:
				found_num=cell_list.index(1)
				cell_list[0] = found_num
				_clear_pencils_after_write(sud,rowindex,colindex,found_num)
				_remains -= 1

def _pen_unique_in_row(sud):
	global _remains
	for k in range(1,10):
		for i in range(9):
			cand = flag = 0
			for j in range(9):
				if sud[i][j][0] == 0 and sud[i][j][k] == 1:
					flag += 1
					cand = j
			if flag == 1:
				sud[i][cand][0] = k
				_clear_pencils_after_write(sud,i,cand,k)
				_remains -= 1

def _pen_unique_in_column(sud):
	global _remains
	for k in range(1,10):
		for j in range(9):
			cand = flag = 0
			for i in range(9):
				if sud[i][j][0] == 0 and sud[i][j][k] == 1:
					flag += 1
					cand = i
			if flag == 1:
				sud[cand][j][0] = k
				_clear_pencils_after_write(sud,cand,j,k)
				_remains -= 1

def _pen_unique_in_box(sud,i,j):
	global _remains
	i_top=i+3
	j_top=j+3
	for k in range(1,10):
		flag = candx = candy = 0
		for x in range(i,i_top):
			for y in range(j,j_top):
				if not sud[x][y][0] and sud[x][y][k]:
					flag += 1
					candx = x
					candy = y
		if flag == 1:
			sud[candx][candy][0] = k
			_clear_pencils_after_write(sud,candx,candy,k)
			_remains -= 1

def solve(sudoku):
	global _remains
	prevrem = 0
	for row in sudoku:
		for cell in row:
			if cell == 0:
				_remains += 1
	sud=_construct_sudoku(sudoku)
	while _remains:
		_pencil(sud)
		_pen(sud)
		_pen_unique_in_row(sud)
		_pen_unique_in_column(sud)
		for x in range(0,9,3):
			for y in range(0,9,3):
				_pen_unique_in_box(sud,x,y)
		if prevrem == _remains:
			break
		else:
			prevrem = _remains
	ret=_deconstruct_sudoku(sud)
	return ret