import pygame, pygame_menu, time, random, sys

pygame.init()

class Gambar:
    def __init__(self, gambar, pos):
        self.gambar = gambar
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.rect = self.gambar.get_rect(center=(self.pos_x, self.pos_y))
    
    def update(self, layar):
        if self.gambar is not None:
            layar.blit(self.gambar, self.rect)
    
    def checkinput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

class TombolText:
	def __init__(self, gambar, pos, text_input, font, warna_utama, warna_hover, posisi_text):
		self.gambar = gambar
		self.pos_x = pos[0]
		self.pos_y = pos[1]
		self.font = font
		self.warna_utama, self.warna_hover = warna_utama, warna_hover
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.warna_utama)
		self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
		self.posisi_text = posisi_text
		if self.gambar is None:
			self.gambar = self.text
		self.rect = self.gambar.get_rect(center=(self.pos_x, self.pos_y))
		if self.posisi_text is not None:
		    self.text_rect = self.text.get_rect(center=(posisi_text[0], posisi_text[1]))

	def update(self, screen):
		if self.gambar is not None:
			layar.blit(self.gambar, self.rect)
		layar.blit(self.text, self.text_rect)

	def checkinput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.warna_hover)
		else:
			self.text = self.font.render(self.text_input, True, self.warna_utama)

def get_font(name, size):
    if name == "Spartan":
        return pygame.font.Font("font/LeagueSpartan-Bold.ttf", size)
    elif name == "Amsterdam":
        return pygame.font.Font("font/Amsterdam.ttf", size)
    return pygame.font.Font("font/font.ttf", size)

tinggi = 1369
lebar = 720
tinggi_papan = 610
lebar_papan = 610
tinggi_xo = (tinggi_papan/3)-((tinggi_papan/3)/2)/2
lebar_xo = (lebar_papan/3)-((lebar_papan/3)/2)/2
tinggi_player_icon = tinggi_xo/2+30
lebar_player_icon = lebar_xo/2+30
lebar_rectangle = lebar_papan-50
tinggi_rectangle = (tinggi_papan/2)+30

counter = 15
pygame.time.set_timer(pygame.USEREVENT, 1000)

xo = "x"
pemenang = None
seri = None
lawan_bot = False
resume_pause = False
EVENTUSER = False
baris_click_temp, kolom_click_temp = None, None

hitam = (0,0,0)
putih = (255, 255, 255)

board = [[None]*3, [None]*3, [None]*3]
fps = 60
CLOCK = pygame.time.Clock()

layar = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Tic Tac Toe Android")

gameplay_bg = pygame.image.load("gambar/surface.jpg")
play = pygame.image.load("gambar/play.png")
pause = pygame.image.load("gambar/pause.png")
menu_layar = pygame.image.load("gambar/menu.jpg")
vs_1 = pygame.image.load("gambar/1v1.png")
vs_bot = pygame.image.load("gambar/vs_bot.png")
gambar_pengaturan = pygame.image.load("gambar/pause_icon.png")
rect_img = pygame.image.load("gambar/rectangle.png")
initiating_window = pygame.image.load("gambar/Tic_Tac_Toe.jpg")
x_img = pygame.image.load("gambar/x.png")
o_img = pygame.image.load("gambar/o.png")

gameplay_bg = pygame.transform.scale(gameplay_bg, (lebar, tinggi))
play = pygame.transform.scale(play, (lebar_xo/2, tinggi_xo/2))
pause = pygame.transform.scale(pause, (lebar_papan/1.2, tinggi_papan/1.2))
gameplay_rect = gameplay_bg.get_rect(center=(lebar/2, tinggi/2))
menu_layar = pygame.transform.scale(menu_layar, (lebar, tinggi))
menu_rect = menu_layar.get_rect(center=(lebar/2, tinggi/2))
vs_1 = pygame.transform.scale(vs_1, (lebar_xo, tinggi_xo))
vs_bot = pygame.transform.scale(vs_bot, (lebar_xo, tinggi_xo))
gambar_pengaturan = pygame.transform.scale(gambar_pengaturan, (lebar_xo/2, tinggi_xo/2))
rect_img = pygame.transform.scale(rect_img, (lebar_rectangle, tinggi_rectangle))
initiating_window = pygame.transform.scale(initiating_window, (lebar_papan, tinggi_papan))
initiating_window_rect = initiating_window.get_rect(center=(lebar/2, tinggi/2))
x_img = pygame.transform.scale(x_img, (lebar_xo, tinggi_xo))
o_img = pygame.transform.scale(o_img, (lebar_xo, tinggi_xo))

mainlagi = TombolText(gambar=None, pos=(lebar/2, tinggi*0.6), text_input="Main Lagi", font=get_font(None, 40), warna_utama="White", warna_hover="Green", posisi_text=None)
kembali_setelah = TombolText(gambar=None, pos=(lebar/2, tinggi*0.7), text_input="Kembali", font=get_font(None, 40), warna_utama="White", warna_hover="Green", posisi_text=None)

title_pause = get_font(None, 40).render("PAUSED", True, "Red")
title_pause_rect = title_pause.get_rect(center=(lebar/2, ((tinggi-(tinggi_papan/1.2))/2)+(tinggi_papan/1.2)/3.7))
pause_rect = pause.get_rect(center=(lebar/2, tinggi/2))
resume_button = TombolText(gambar=None, pos=(((lebar-(lebar_papan/1.2))/2)+(lebar_papan/1.2)/2, ((tinggi-(tinggi_papan/1.2))/2)+(tinggi_papan/1.2)/2.25), text_input="Resume", font=get_font(None, 30), warna_utama="White", warna_hover="Green", posisi_text=None)
backmenu_button = TombolText(gambar=None, pos=(((lebar-(lebar_papan/1.2))/2)+(lebar_papan/1.2)/2, ((tinggi-(tinggi_papan/1.2))/2)+(tinggi_papan/1.2)/1.75), text_input="Menu", font=get_font(None, 30), warna_utama="White", warna_hover="Green", posisi_text=None)

play_resume = Gambar(gambar=play, pos=((lebar_xo/2)/2+10, (tinggi_xo/2)/2+10))
pengaturan = Gambar(gambar=gambar_pengaturan, pos=((lebar_xo/2)/2+10, (tinggi_xo/2)/2+10))

rectangle = Gambar(gambar=rect_img, pos=(lebar/2, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2))

waktu_x = get_font(None, 35).render("~", True, "Red")
waktu_o = get_font(None, 35).render("~", True, "Red")
waktu_rect_x = waktu_x.get_rect(center=(lebar/2/2+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_player_icon/2)-18))
waktu_rect_o = waktu_o.get_rect(center=((lebar/2)+((lebar/2)/2)+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_player_icon/2)-18))

rect_x = (128, 128, 128)
rect_o = (128, 128, 128)

player_icons_x = TombolText(gambar=None, pos=((lebar/2)/2+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2+1), text_input="X", font=get_font(None, 45), warna_utama="Red", warna_hover="Green", posisi_text=None)

player_icons_o = TombolText(gambar=None, pos=((lebar/2)+((lebar/2)/2)+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2+1), text_input="O", font=get_font(None, 45), warna_utama="Red", warna_hover="Green", posisi_text=None)

title = get_font("Spartan", 80).render("TIC TAC TOE", True, "Orange")
title2 = get_font("Amsterdam", 65).render("Classic Game", True, "White")
title_rect = title.get_rect(center=(lebar/2, tinggi*0.1))
title2_rect = title2.get_rect(center=(lebar/2, tinggi*0.13))
play = TombolText(gambar=None, pos=(lebar/2, tinggi*0.24), text_input="PLAY", font=get_font("Spartan", 55), warna_utama="White", warna_hover="Green", posisi_text=None)
quit = TombolText(gambar=None, pos=(lebar/2, tinggi*0.285), text_input="QUIT", font=get_font("Spartan", 55), warna_utama="White", warna_hover="Green", posisi_text=None)

title_mode = get_font("Spartan", 60).render("PILIH MODE", True, "Orange")
title_mode_rect = title_mode.get_rect(center=(lebar/2, tinggi*0.1))
mode_1v1 = TombolText(gambar=vs_1, pos=(lebar*0.40, tinggi*0.255), text_input="1 VS 1", font=get_font("Amsterdam", 65), warna_utama="White", warna_hover="Green", posisi_text=((lebar*0.40)-(lebar_xo/2)+5, (tinggi*0.255)+(tinggi_xo/2)-5))
mode_vsbot = TombolText(gambar=vs_bot, pos=(lebar*0.30, tinggi*0.41), text_input="VS BOT", font=get_font("Amsterdam", 65), warna_utama="White", warna_hover="Green", posisi_text=((lebar*0.30)+(lebar_xo/2)+5, (tinggi*0.41)+(tinggi_xo/2)-5))
back = TombolText(gambar=None, pos=(lebar*0.35, tinggi*0.54), text_input="MENU UTAMA", font=get_font("Spartan", 45), warna_utama="White", warna_hover="Green", posisi_text=None)

player_vs = "vs"
player_vs_text = get_font(None, 45).render(player_vs, True, "Red")
player_vs_rect = player_vs_text.get_rect(center=(lebar/2, (tinggi-tinggi_papan)/2/2+((tinggi_papan/3)/2)/2/2))

score_x, score_o = 0, 0

lampu = "•"
lampu_text_x = get_font(None, 50).render(lampu, True, "Red")
lampu_text_o = get_font(None, 50).render(lampu, True, "Red")
lampu_rect_x = lampu_text_x.get_rect(center=((lebar/2)/2-1, ((tinggi-tinggi_papan)/2)/2+((tinggi_player_icon/2)-3)*2))
lampu_rect_o = lampu_text_o.get_rect(center=((lebar/2)+((lebar/2)/2)-1, ((tinggi-tinggi_papan)/2)/2+((tinggi_player_icon/2)-3)*2))

def status():
    global seri
    
    if pemenang is None:
        pesan = "Giliran " + xo.upper()
    else:
        pesan = pemenang.upper() + " Menang"
    if seri:
        pesan = "Game Seri"
        
    font = get_font(None, 45)
    text = font.render(pesan, 1, hitam)
    
    text_rect = text.get_rect(center=(lebar/2, (tinggi-tinggi_papan)/2+tinggi_papan+((tinggi-tinggi_papan)/2)/2))
    layar.blit(text, text_rect)
    if resume_pause:
        pass
    else:
        pygame.display.update()

def check_win():
    global board, pemenang, seri
    
    for baris in range(3):
        if board[baris][0] == board[baris][1] == board[baris][2] and board[baris][0] is not None:
            pemenang = board[baris][0]
            pygame.draw.line(layar, hitam, ((lebar-lebar_papan)/2, ((tinggi-tinggi_papan)/2)+(((baris+1)*(tinggi_papan/3))-((tinggi_papan/3)/2))), ((lebar-lebar_papan)/2+lebar_papan, ((tinggi-tinggi_papan)/2)+(((baris+1)*(tinggi_papan/3))-((tinggi_papan/3)/2))), 7)
            break
            
    for kolom in range(3):
        if board[0][kolom] == board[1][kolom] == board[2][kolom] and board[0][kolom] is not None:
            pemenang = board[0][kolom]
            pygame.draw.line(layar, hitam, (((lebar-lebar_papan)/2)+((kolom+1)*(lebar_papan/3))-((lebar_papan/3)/2), (tinggi-tinggi_papan)/2), (((lebar-lebar_papan)/2)+((kolom+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2+tinggi_papan)), 7)
            break
            
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        pemenang = board[0][0]
        pygame.draw.line(layar, hitam, ((lebar-lebar_papan)/2, (tinggi-tinggi_papan)/2), ((lebar-lebar_papan)/2+lebar_papan, (tinggi-tinggi_papan)/2+tinggi_papan), 7)
        
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        pemenang = board[0][2]
        pygame.draw.line(layar, hitam, ((lebar-lebar_papan)/2+lebar_papan, (tinggi-tinggi_papan)/2), ((lebar-lebar_papan)/2, (tinggi-tinggi_papan)/2+tinggi_papan), 7)
    
    if all([all(baris) for baris in board]) and pemenang is None:
        seri = True
    status()

def gambarxo(baris, kolom):
    global board, xo
    
    if baris == 1:
        posx = (((tinggi_papan/3)-(tinggi_xo))/2)+((tinggi-tinggi_papan)/2)
    elif baris == 2:
        posx = (((tinggi_papan/3)-(tinggi_xo))/2)+((tinggi-tinggi_papan)/2)+(tinggi_papan/3)
    elif baris == 3:
        posx = (((tinggi_papan/3)-(tinggi_xo))/2)+((tinggi-tinggi_papan)/2)+((tinggi_papan/3)*2)
    if kolom == 1:
        posy = (((lebar_papan/3)-(lebar_xo))/2)+((lebar-lebar_papan)/2)
    elif kolom == 2:
        posy = (((lebar_papan/3)-(lebar_xo))/2)+((lebar-lebar_papan)/2)+(lebar_papan/3)
    elif kolom == 3:
        posy = (((lebar_papan/3)-(lebar_xo))/2)+((lebar-lebar_papan)/2)+((lebar_papan/3)*2)
    
    if resume_pause:
        pass
    else:
        board[baris-1][kolom-1] = xo
    if resume_pause:
        if board[baris-1][kolom-1] == "x":
            layar.blit(x_img, (posy, posx))
        else:
            layar.blit(o_img, (posy, posx))
    else:
        if xo == "x":
            layar.blit(x_img, (posy, posx))
            xo = "o"
        else:
            layar.blit(o_img, (posy, posx))
            xo = "x"
    pygame.display.update()

def baris_kolom(x, y):
    baris = None
    kolom = None
    
    if x <= (lebar_papan/3)+((lebar-lebar_papan)/2) and x >= ((lebar-lebar_papan)/2):
        kolom = 1
    elif x <= (lebar_papan/3*2)+((lebar-lebar_papan)/2) and x >= ((lebar-lebar_papan)/2):
        kolom = 2
    elif x <= lebar_papan+((lebar-lebar_papan)/2) and x >= ((lebar-lebar_papan)/2):
        kolom = 3
    else:
        kolom = None
    if y <= (tinggi_papan/3)+((tinggi-tinggi_papan)/2) and y >= ((tinggi-tinggi_papan)/2):
        baris = 1
    elif y <= (tinggi_papan/3*2)+((tinggi-tinggi_papan)/2) and y >= ((tinggi-tinggi_papan)/2):
        baris = 2
    elif y <= tinggi_papan+((tinggi-tinggi_papan)/2) and y >= ((tinggi-tinggi_papan)/2):
        baris = 3
    else:
        baris = None
    return baris, kolom

def bot_o(baris, kolom):
    # Cek o
    for b in range(3):
        if board[b][0] == board[b][1] and board[b][0] == "o" and board[b][2] is None:
            return ((lebar-lebar_papan)/2)+(lebar_papan-((lebar_papan/3)/2)), ((tinggi-tinggi_papan)/2)+((b+1)*(tinggi_papan/3))-((tinggi_papan/3)/2)
        elif board[b][0] == board[b][2] and board[b][0] == "o" and board[b][1] is None:
            return ((lebar-lebar_papan)/2)+(lebar_papan/2), ((tinggi-tinggi_papan)/2)+((b+1)*(tinggi_papan/3))-((tinggi_papan/3)/2)
        elif board[b][1] == board[b][2] and board[b][1] == "o" and board[b][0] is None:
            return ((lebar-lebar_papan)/2)+((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+((b+1)*(tinggi_papan/3))-((tinggi_papan/3)/2)
    
    for k in range(3):
        if board[0][k] == board[1][k] and board[0][k] == "o" and board[2][k] is None:
            return ((lebar-lebar_papan)/2)+((k+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan-((tinggi_papan/3)/2))
        elif board[0][k] == board[2][k] and board[0][k] == "o" and board[1][k] is None:
            return ((lebar-lebar_papan)/2)+((k+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan/2)
        elif board[1][k] == board[2][k] and board[1][k] == "o" and board[0][k] is None:
            return ((lebar-lebar_papan)/2)+((k+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)/2)
    
    # Cek o dan x   
    if board[0][0] == board[1][1] and board[2][2] is None and board[0][0] == "o":
        return ((lebar-lebar_papan)/2)+(lebar_papan-((lebar_papan/3)/2)), ((tinggi-tinggi_papan)/2)+(tinggi_papan-((tinggi_papan/3)/2))
    elif board[0][0] == board[2][2] and board[1][1] is None and board[0][0] == "o":
        return ((lebar-lebar_papan)/2)+(lebar_papan/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan/2)
    elif board[1][1] == board[2][2] and board[0][0] is None and board[1][1] == "o":
        return ((lebar-lebar_papan)/2)+((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)/2)
    
    if board[0][2] == board[1][1] and board[2][0] is None and board[0][2] == "o":
        return ((lebar-lebar_papan)/2)+((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan-((tinggi_papan/3)/2))
    elif board[0][2] == board[2][0] and board[1][1] is None and board[0][2] == "o":
        return ((lebar-lebar_papan)/2)+(lebar_papan/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan/2)
    elif board[1][1] == board[2][0] and board[0][2] is None and board[1][1] == "o":
        return ((lebar-lebar_papan)/2)+(lebar_papan-((lebar_papan/3)/2)), ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)/2)
    
    if board[0][0] == board[1][1] and board[2][2] is None and board[0][0] == "x":
        return ((lebar-lebar_papan)/2)+(lebar_papan-((lebar_papan/3)/2)), ((tinggi-tinggi_papan)/2)+(tinggi_papan-((tinggi_papan/3)/2))
    elif board[0][0] == board[2][2] and board[1][1] is None and board[0][0] == "x":
        return ((lebar-lebar_papan)/2)+(lebar_papan/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan/2)
    elif board[1][1] == board[2][2] and board[0][0] is None and board[1][1] == "x":
        return ((lebar-lebar_papan)/2)+((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)/2)
    
    if board[0][2] == board[1][1] and board[2][0] is None and board[0][2] == "x":
        return ((lebar-lebar_papan)/2)+((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan-((tinggi_papan/3)/2))
    elif board[0][2] == board[2][0] and board[1][1] is None and board[0][2] == "x":
        return ((lebar-lebar_papan)/2)+(lebar_papan/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan/2)
    elif board[1][1] == board[2][0] and board[0][2] is None and board[1][1] == "x":
        return ((lebar-lebar_papan)/2)+(lebar_papan-((lebar_papan/3)/2)), ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)/2)
        
    # Cek x
    if board[baris][0] == board[baris][1] and board[baris][2] is None and board[baris][0] == "x":
        return ((lebar-lebar_papan)/2)+(lebar_papan-((lebar_papan/3)/2)), ((tinggi-tinggi_papan)/2)+((baris+1)*(tinggi_papan/3))-((tinggi_papan/3)/2)
    elif board[baris][0] == board[baris][2] and board[baris][1] is None and board[baris][0] == "x":
        return ((lebar-lebar_papan)/2)+(lebar_papan/2), ((tinggi-tinggi_papan)/2)+((baris+1)*(tinggi_papan/3))-((tinggi_papan/3)/2)
    elif board[baris][1] == board[baris][2] and board[baris][0] is None and board[baris][1] == "x":
        return ((lebar-lebar_papan)/2)+((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+((baris+1)*(tinggi_papan/3))-((tinggi_papan/3)/2)
        
    if board[0][kolom] == board[1][kolom] and board[2][kolom] is None and board[0][kolom] == "x":
        return ((lebar-lebar_papan)/2)+((kolom+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan-((tinggi_papan/3)/2))
    elif board[0][kolom] == board[2][kolom] and board[1][kolom] is None and board[0][kolom] == "x":
        return ((lebar-lebar_papan)/2)+((kolom+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+(tinggi_papan/2)
    elif board[1][kolom] == board[2][kolom] and board[0][kolom] is None and board[1][kolom] == "x":
        return ((lebar-lebar_papan)/2)+((kolom+1)*(lebar_papan/3))-((lebar_papan/3)/2), ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)/2)
        
    while True:
        x_acak = random.randint(int((lebar-lebar_papan)/2), int(((lebar-lebar_papan)/2)+lebar_papan))
        y_acak = random.randint(int((tinggi-tinggi_papan)/2), int(((tinggi-tinggi_papan)/2)+tinggi_papan))
        baris_acak, kolom_acak = baris_kolom(x_acak, y_acak)
        if board[baris_acak-1][kolom_acak-1] is None:
            return x_acak, y_acak

def init_awal():
    global rect_x, rect_o, waktu_x, waktu_o, waktu_rect_x, waktu_rect_o, lampu_text_x, lampu_text_o, lampu_rect_x, lampu_rect_o
    rect_x = (128, 128, 128)
    rect_o = (128, 128, 128)
    
    waktu_x = get_font(None, 35).render("~", True, "Red")
    waktu_o = get_font(None, 35).render("~", True, "Red")
    waktu_rect_x = waktu_x.get_rect(center=(lebar/2/2+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_player_icon/2)-18))
    waktu_rect_o = waktu_o.get_rect(center=((lebar/2)+((lebar/2)/2)+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_player_icon/2)-18))
    
    lampu_text_x = get_font(None, 50).render(lampu, True, "Red")
    lampu_text_o = get_font(None, 50).render(lampu, True, "Red")
    lampu_rect_x = lampu_text_x.get_rect(center=((lebar/2)/2-1, ((tinggi-tinggi_papan)/2)/2+((tinggi_player_icon/2)-3)*2))
    lampu_rect_o = lampu_text_o.get_rect(center=((lebar/2)+((lebar/2)/2)-1, ((tinggi-tinggi_papan)/2)/2+((tinggi_player_icon/2)-3)*2))

def main_lagi():
    global board, pemenang, counter, xo, seri, ket, baris_click_temp, kolom_click_temp
    init_awal()
    game_initiating_window()
    xo = "x"
    seri = False
    pemenang = None
    counter = 15
    board = [[None]*3, [None]*3, [None]*3]
    ket = None
    baris_click_temp = None
    kolom_click_temp = None

def init_menu_utama():
    global xo, seri, pemenang, board, lawan_bot, score_x, score_o, ket, counter, baris_click_temp, kolom_click_temp
    xo = "x"
    seri = False
    pemenang = None
    board = [[None]*3, [None]*3, [None]*3]
    lawan_bot = False
    score_x = 0
    score_o = 0
    ket = None
    counter = 15
    baris_click_temp = None
    kolom_click_temp = None
    init_awal()

def updatexo():
    global lampu_text_x, lampu_text_o, lampu_rect_x, lampu_rect_o, waktu_x, waktu_o, waktu_rect_x, waktu_rect_o, rect_x, rect_o
    if xo == "x":
        waktu_x = get_font(None, 35).render(str(counter), True, "#5ae717")
        lampu_text_x = get_font(None, 50).render(lampu, True, "#5ae717")
        rect_x = "#5ae717"
        waktu_o = get_font(None, 35).render("~", True, "Red")
        lampu_text_o = get_font(None, 50).render(lampu, True, "Red")
        rect_o = (128, 128, 128)
    elif xo == "o":
        waktu_o = get_font(None, 35).render(str(counter), True, "#5ae717")
        lampu_text_o = get_font(None, 50).render(lampu, True, "#5ae717")
        rect_o = "#5ae717"
        waktu_x = get_font(None, 35).render("~", True, "Red")
        lampu_text_x = get_font(None, 50).render(lampu, True, "Red")
        rect_x = (128, 128, 128)
                    
    waktu_rect_x = waktu_x.get_rect(center=(lebar/2/2+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_player_icon/2)-18))
    lampu_rect_x = lampu_text_x.get_rect(center=((lebar/2)/2-1, ((tinggi-tinggi_papan)/2)/2+((tinggi_player_icon/2)-3)*2))
    waktu_rect_o = waktu_o.get_rect(center=((lebar/2)+((lebar/2)/2)+1, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_player_icon/2)-18))
    lampu_rect_o = lampu_text_o.get_rect(center=((lebar/2)+((lebar/2)/2)-1, ((tinggi-tinggi_papan)/2)/2+((tinggi_player_icon/2)-3)*2))

def apakah_berakhir():
    global score_x, score_o, ket, title_win, title_win_rect
    if pemenang or seri:
        if pemenang == "x":
            score_x += 1
            if lawan_bot:
                ket = "Kamu Menang"
            else:
                ket = "X Menang"
        elif pemenang == "o":
            score_o += 1
            if lawan_bot:
                ket = "Kamu Kalah"
            else:
                ket = "O Menang"
        else:
            ket = "Seri"
        title_win = get_font(None, 55).render(ket, True, "Orange")
        title_win_rect = title_win.get_rect(center=(lebar/2, tinggi*0.225))
        main_lagi_kah = setelah_main()
        if main_lagi_kah:
            main_lagi()
        tampilkan_informasi()

def game_initiating_window():
    if EVENTUSER:
        updatexo()
        
    else:
        layar.blit(gameplay_bg, gameplay_rect)
        layar.blit(initiating_window, initiating_window_rect)
        pengaturan.update(layar)
        
    rectangle.update(layar)
    player_icons_x.update(layar)
    player_icons_o.update(layar)
    
    layar.blit(player_vs_text, player_vs_rect)
    
    score_text = get_font(None, 30).render(str(score_x) + ":" + str(score_o), True, "Red")
    score_rect = score_text.get_rect(center=(lebar/2, ((tinggi-tinggi_papan)/2)/2+((tinggi_papan/3)/2)/2/2-(tinggi_rectangle/2/2)))
    layar.blit(score_text, score_rect)
    
    layar.blit(waktu_x, waktu_rect_x)
    layar.blit(waktu_o, waktu_rect_o)
    layar.blit(lampu_text_x, lampu_rect_x)
    layar.blit(lampu_text_o, lampu_rect_o)
    
    #Border Player Icon
    pygame.draw.rect(layar, rect_x, pygame.Rect(((lebar/2)/2)-(lebar_player_icon/2), (((tinggi-tinggi_papan)/2)/2)-(tinggi_player_icon/2)+((tinggi_papan/3)/2)/2/2, lebar_player_icon, tinggi_player_icon), 5, 18)
    pygame.draw.rect(layar, rect_o, pygame.Rect(((lebar/2)+((lebar/2)/2))-(lebar_player_icon/2), (((tinggi-tinggi_papan)/2)/2)-(tinggi_player_icon/2)+((tinggi_papan/3)/2)/2/2, lebar_player_icon, tinggi_player_icon), 5, 18)
    
    if EVENTUSER:
        pass
    else:
        # Border Board
        pygame.draw.rect(layar, hitam, pygame.Rect((lebar-lebar_papan)/2, (tinggi-tinggi_papan)/2, lebar_papan, tinggi_papan), 5, 4)
        
        # Kolom Vertikal
        pygame.draw.line(layar, hitam, (((lebar-lebar_papan)/2)+(lebar_papan/3), (tinggi-tinggi_papan)/2), (((lebar-lebar_papan)/2)+(lebar_papan/3), ((tinggi-tinggi_papan)/2)+tinggi_papan), 5)
        pygame.draw.line(layar, hitam, (((lebar-lebar_papan)/2)+((lebar_papan/3)*2), (tinggi-tinggi_papan)/2), (((lebar-lebar_papan)/2)+((lebar_papan/3)*2), ((tinggi-tinggi_papan)/2)+tinggi_papan), 5)
        
        # Baris Horizontal
        pygame.draw.line(layar, hitam, ((lebar-lebar_papan)/2, ((tinggi-tinggi_papan)/2)+(tinggi_papan/3)), (((lebar-lebar_papan)/2)+lebar_papan, ((tinggi-tinggi_papan)/2)+(tinggi_papan/3)), 5)
        pygame.draw.line(layar, hitam, ((lebar-lebar_papan)/2, ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)*2)), (((lebar-lebar_papan)/2)+lebar_papan, ((tinggi-tinggi_papan)/2)+((tinggi_papan/3)*2)), 5)
    
    status()

def user_click(x, y):
    global counter, baris_click_temp, kolom_click_temp
    
    while True:
        baris_temp, kolom_temp = baris_kolom(x, y)
        if baris_temp and kolom_temp and board[baris_temp-1][kolom_temp-1] is None:
            baris_click_temp, kolom_click_temp = baris_temp, kolom_temp
        break
    
    while True:
        baris_click, kolom_click = baris_kolom(x, y)
        if baris_click and kolom_click and board[baris_click-1][kolom_click-1] is None:
            gambarxo(baris_click, kolom_click)
            check_win()
            counter = 15
        if xo == "x":
            break
        else:
            if pemenang or seri:
                break
            else:
                if lawan_bot:
                    x, y = bot_o(baris_click-1, kolom_click-1)
                else:
                    break

def main():
    global counter, xo, EVENTUSER, baris_click_temp, kolom_click_temp
    game_initiating_window()
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
            
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
                
            elif ev.type == pygame.USEREVENT:
                counter -= 1
                
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                MOUSE_POS = pygame.mouse.get_pos()
                if pengaturan.checkinput(MOUSE_POS):
                    paused()
                user_click(MOUSE_POS[0], MOUSE_POS[1])
                tampilkan_informasi()
                apakah_berakhir()
        
        if counter < 0:
            if xo == "x":
                xo = "o"
                if lawan_bot:
                    if baris_click_temp is None and kolom_click_temp is None:
                        while True:
                            baris_click_temp, kolom_click_temp = random.randint(1, 3), random.randint(1, 3)
                            if board[baris_click_temp-1][kolom_click_temp-1] is None:
                                break
                    elif board[baris_click_temp-1][kolom_click_temp-1] is not None:
                        while True:
                            baris_click_temp, kolom_click_temp = random.randint(1, 3), random.randint(1, 3)
                            if board[baris_click_temp-1][kolom_click_temp-1] is None:
                                break
                    x_temp, y_temp = bot_o(baris_click_temp-1, kolom_click_temp-1)
                    baris_click_bot, kolom_click_bot = baris_kolom(x_temp, y_temp)
                    gambarxo(baris_click_bot, kolom_click_bot)
                    tampilkan_informasi()
                    apakah_berakhir()
                    
            elif xo == "o":
                xo = "x"
            counter = 15
            
        EVENTUSER = True
        game_initiating_window()
        EVENTUSER = False
        
        CLOCK.tick(fps)

def tampilkan_informasi():
    global resume_pause
    resume_pause = True
    game_initiating_window()
    for baris in range(1, 4):
        for kolom in range(1, 4):
            if board[baris-1][kolom-1] is not None:
                gambarxo(baris, kolom)
    check_win()
    resume_pause = False

"""
======================================================
======================================================
MENU
"""

def setelah_main():
    layar.blit(title_win, title_win_rect)
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if mainlagi.checkinput(MOUSE_POS):
                    return True
                if kembali_setelah.checkinput(MOUSE_POS):
                    menu_utama()
            for button in [mainlagi, kembali_setelah]:
                button.changeColor(MOUSE_POS)
                button.update(layar)
        pygame.display.update()

def paused():
    not_resume = True
    play_resume.update(layar)
    layar.blit(pause, pause_rect)
    layar.blit(title_pause, title_pause_rect)
    while not_resume:
        MOUSE_POS = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if play_resume.checkinput(MOUSE_POS):
                    not_resume = False
                    tampilkan_informasi()
                if resume_button.checkinput(MOUSE_POS):
                    not_resume = False
                    tampilkan_informasi()
                if backmenu_button.checkinput(MOUSE_POS):
                    menu_utama()
        if not_resume:
            for button in [resume_button, backmenu_button]:
                button.changeColor(MOUSE_POS)
                button.update(layar)
        pygame.display.update()

def pilih_mode():
    global lawan_bot
    layar.blit(menu_layar, menu_rect)
    layar.blit(title_mode, title_mode_rect)
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if mode_1v1.checkinput(MOUSE_POS):
                    main()
                if mode_vsbot.checkinput(MOUSE_POS):
                    lawan_bot = True
                    main()
                if back.checkinput(MOUSE_POS):
                    menu_utama()
        for button in [mode_1v1, mode_vsbot, back]:
            button.changeColor(MOUSE_POS)
            button.update(layar)
        pygame.display.update()

def menu_utama():
    init_menu_utama()
    layar.blit(menu_layar, menu_rect)
    layar.blit(title, title_rect)
    layar.blit(title2, title2_rect)
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if play.checkinput(MOUSE_POS):
                    pilih_mode()
                if quit.checkinput(MOUSE_POS):
                    sys.exit()
        for button in [play, quit]:
            button.changeColor(MOUSE_POS)
            button.update(layar)
        pygame.display.update()

menu_utama()