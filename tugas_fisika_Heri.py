"""
TUGAS AKHIR FISIKA - SEMESTER GANJIL 2025/2026
IDENTITAS MAHASISWA:
Nama  : HERI ARIYANTO
NIM   : A18.2025.00172
Kelas : PJJ UDINUS
Tema  : Pegas (Hukum Hooke, Seri-Paralel & Osilasi)
"""

import pygame
import math

# --- 1. INISIALISASI ---
pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tugas Akhir Fisika - Heri Ariyanto")
font_small = pygame.font.SysFont("Consolas", 16)
font_mid = pygame.font.SysFont("Consolas", 20, bold=True)

# Warna Tema Modern
BG_COLOR, BOX_COLOR = (30, 30, 30), (10, 10, 10)
WHITE, BLUE, RED, CYAN, GRAY = (255, 255, 255), (0, 102, 204), (200, 0, 0), (0, 255, 255), (100, 100, 100)

# --- 2. KELAS SLIDER ---
class Slider:
    def __init__(self, x, y, w, min_val, max_val, label, unit, current_val):
        self.rect = pygame.Rect(x, y, w, 10)
        self.min, self.max = min_val, max_val
        self.val = current_val
        self.label, self.unit = label, unit
        self.grabbed = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pos_x = self.rect.x + (self.val - self.min) / (self.max - self.min) * self.rect.w
        pygame.draw.circle(screen, BLUE, (int(pos_x), self.rect.y + 5), 10)
        text = font_small.render(f"{self.label}: {self.val:.1f} {self.unit}", True, WHITE)
        screen.blit(text, (self.rect.x, self.rect.y - 25))

    def update(self, m_pos, m_click):
        if m_click[0] and self.rect.collidepoint(m_pos): self.grabbed = True
        if not m_click[0]: self.grabbed = False
        if self.grabbed:
            rel_x = max(0, min(m_pos[0] - self.rect.x, self.rect.w))
            self.val = self.min + (rel_x / self.rect.w) * (self.max - self.min)

# Inisialisasi Slider & State
s_k = Slider(450, 480, 200, 10, 200, "Konstanta (k)", "N/m", 100.0)
s_m = Slider(450, 540, 200, 0.5, 10, "Massa (m)", "kg", 2.0)
mode = "SINGLE" # Mode: SINGLE, SERI, PARALEL
t_sim = 0.0
is_moving = False
points = []

def draw_spring(start_x, start_y, end_y, segments=15):
    px_prev, py_prev = start_x, start_y
    for i in range(1, segments + 1):
        curr_py = start_y + (i * (end_y - start_y) / segments)
        curr_px = start_x + (20 if i % 2 == 0 else -20)
        if i == segments: curr_px = start_x
        pygame.draw.line(screen, WHITE, (px_prev, py_prev), (curr_px, curr_py), 2)
        px_prev, py_prev = curr_px, curr_py

# --- 3. MAIN LOOP ---
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)
    m_pos, m_click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: is_moving = not is_moving
            if event.key == pygame.K_1: mode = "SINGLE"; points = []
            if event.key == pygame.K_2: mode = "SERI"; points = []
            if event.key == pygame.K_3: mode = "PARALEL"; points = []

    # --- LOGIKA FISIKA (KONSTANTA EFEKTIF) ---
    k_input = s_k.val
    m_val = s_m.val
    
    if mode == "SINGLE":
        k_eff = k_input
    elif mode == "SERI":
        # Rumus: 1/k_eff = 1/k + 1/k -> k_eff = k/2
        k_eff = k_input / 2
    elif mode == "PARALEL":
        # Rumus: k_eff = k + k -> k_eff = 2k
        k_eff = k_input * 2

    omega = math.sqrt(k_eff / m_val)
    period = 2 * math.pi / omega
    
    if is_moving:
        pos_y = 40 * math.cos(omega * t_sim)
        t_sim += 0.05
        points.append(pos_y)
        if len(points) > 300: points.pop(0)
    else: pos_y = 40

    # --- VISUALISASI ---
    sim_rect = pygame.Rect(50, 50, 1000, 350)
    pygame.draw.rect(screen, BOX_COLOR, sim_rect)
    pygame.draw.rect(screen, GRAY, sim_rect, 2)

    y_base = 200 + pos_y
    if mode == "SINGLE":
        draw_spring(250, 50, y_base)
    elif mode == "SERI":
        mid_y = 50 + (y_base - 50)/2
        draw_spring(250, 50, mid_y, 10)
        draw_spring(250, mid_y, y_base, 10)
    elif mode == "PARALEL":
        draw_spring(220, 50, y_base)
        draw_spring(280, 50, y_base)

    pygame.draw.rect(screen, RED, (250 - 25, y_base, 50, 50))

    # Grafik Posisi-Waktu
    if len(points) > 2:
        for i in range(len(points)-1):
            pygame.draw.line(screen, CYAN, (450+i*1.8, 225+points[i]), (450+(i+1)*1.8, 225+points[i+1]), 2)

    # --- UI & DATA OUTPUT ---
    s_k.update(m_pos, m_click); s_k.draw(screen)
    s_m.update(m_pos, m_click); s_m.draw(screen)

    # Identitas & Instruksi
    screen.blit(font_mid.render("IDENTITAS MAHASISWA", True, BLUE), (50, 460))
    for i, t in enumerate([f"Nama : Heri Ariyanto", f"NIM  : A18.2025.00172", f"Kelas: PJJ UDINUS"]):
        screen.blit(font_small.render(t, True, WHITE), (50, 490 + i*25))
    
    screen.blit(font_small.render("TEKAN TOMBOL: [1] Single [2] Seri [3] Paralel", True, CYAN), (50, 600))
    screen.blit(font_small.render("SPASI: Mulai/Pause Osilasi", True, WHITE), (50, 630))

    # Hasil Perhitungan
    screen.blit(font_mid.render("DATA OUTPUT", True, CYAN), (700, 460))
    res_txt = [
        f"Mode Susunan   : {mode}",
        f"k Efektif      : {k_eff:.2f} N/m",
        f"Frekuensi Sudut: {omega:.2f} rad/s",
        f"Periode (T)    : {period:.2f} s",
        f"Gaya Hooke (F) : {k_eff * (abs(pos_y)/10):.2f} N"
    ]
    for i, t in enumerate(res_txt):
        screen.blit(font_small.render(t, True, WHITE), (700, 490 + i*25))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()