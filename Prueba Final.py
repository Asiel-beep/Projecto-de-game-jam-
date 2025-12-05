
import pygame, sys, os, csv, random, time

pygame.init()
pygame.mixer.init()  # por si luego quieres sonidos (no obligatorio)


# VENTANA (estilo móvil)
WIDTH, HEIGHT = 420, 870
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("¿Sabes o No Sabes? - Full")
clock = pygame.time.Clock()
FPS = 60


LOGO_PATH = "/mnt/data/23c82479-f174-4b9d-9bbb-cc78960b8be1.png"

#TIPOGRAFIA
GRADIENT_TOP = (82, 184, 190)
GRADIENT_BOTTOM = (54, 109, 167)
BTN_LEFT = (113, 206, 196)
BTN_RIGHT = (80, 160, 220)
BTN_GLOW = (130, 220, 230, 90)
TEXT_BLACK = (20, 20, 20)
ACCENT = (20, 160, 190)
CORRECT = (120, 200, 150)
WRONG = (240, 100, 110)
CARD_ALPHA = 14

def load_font(name=None, size=26, bold=False):
    try:
        return pygame.font.SysFont("Montserrat", size, bold=bold)
    except:
        return pygame.font.SysFont(None, size, bold=bold)

FONT_TITLE = load_font(size=44, bold=True)
FONT_MED = load_font(size=28)
FONT_SMALL = load_font(size=18)


# CARGA DE PREGUNTAS
DEFAULT_QUESTIONS = [
    {"q": "¿Cuál es la capital de Francia?", "choices": ["París","Madrid","Roma","Berlín"], "answer":0},
    {"q": "¿Cuál es 5 × 6?", "choices": ["11","30","56","22"], "answer":1},
    {"q": "¿Quién pintó la Mona Lisa?", "choices": ["Leonardo Da Vinci","Vincent Van Gogh","Leonardo DiCaprio","Miguel Ángel"], "answer":0},
    {"q": "¿Idioma oficial de Brasil?", "choices": ["Portugués","Español","Inglés","Francés"], "answer":0},
    {"q": "¿Cuál es el país con mayor población en el mundo?", "choices": ["India", "Colombia", "China", "Japón"], "answer":2},
    {"q": "¿Quién escribió “Don Quijote de la Mancha”", "choices": ["William Shakespears", "Miguel de Cervantes", "Edgar Allan Poe", "Agatha Christie"], "answer": 1},
    {"q": "¿Qué planeta es conocido como el planeta rojo?", "choices": ["Tierra", "Venus", "Marte", "Júpiter"], "answer": 2},
    {"q": "¿Cuál es el símbolo químico del oro?", "choices": ["Ag", "O", "Mg", "Au"], "answer":3},
    {"q": "¿Cuál es el idioma más hablado en el mundo?","choices":  ["Inglés", "Español", "Chino mandarín", "Portugués"],"answer": 2},
    {"q": "¿Cuál es la capital de Turquía?", "choices": ["Ag", "O", "Mg", "Au"], "answer": 3},
    {"q": "¿Qué fruta es famosa por ser amarilla y curvada?", "choices": ["Plátano", "Piña", "Kiwi", "Manzana"], "answer": 0},
    {"q": "¿Cuál es el metal más utilizado para fabricar cables eléctricos?", "choices":  ["Oro", "Cobre", "Plata", "Estaño"], "answer": 1},
    {"q": "¿Cuál es la moneda oficial de Estados Unidos?", "choices": ["Peso", "Euro", "Dólar", "Libra"], "answer": 2},
    {"q": "¿Qué instrumento mide la temperatura?", "choices":  ["Cronómetro", "Barómetro", "Balanza", "Termómetro"], "answer": 3},
    {"q": "¿Qué animal pone huevos y tiene plumas?", "choices": ["Perro", "Gato", "Gallina", "Murciélago"],"answer": 2},
    {"q": "¿Qué año llegó Cristóbal Colón a América?", "choices": ["1492", "1536", "1412", "1821"],"answer": 0},
    {"q": "¿Qué número romano representa el 10?", "choices": ["IX", "D", "X", "VIII"],"answer": 3},
    {"q": "¿Cuál es la capital de Argentina?", "choices": ["Córdoba", "Buenos Aires", "Mar de Plata", "Lima"],"answer": 1},
    {"q": "¿Cuál es el deporte más popular del mundo?", "choices": ["Béisbol", "Voleibol", "Tenis", "Fútbol"],"answer": 3},
    {"q": "¿Qué continente es el más grande?", "choices": ["América", "Asia", "África", "Oceanía"],"answer": 1},
]

CSV_PATH = "/mnt/data/questions.csv"

def load_questions():
    if os.path.exists(CSV_PATH):
        try:
            qs = []
            with open(CSV_PATH, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Formato esperado por fila: pregunta, opcion1, opcion2, opcion3, opcion4, index_correct (0-3)
                for row in reader:
                    if len(row) >= 6:
                        q = row[0].strip()
                        choices = [row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()]
                        try:
                            ans = int(row[5])
                        except:
                            ans = 0
                        qs.append({"q": q, "choices": choices, "answer": ans})
            if len(qs) > 0:
                return qs
        except Exception as e:
            print("Error leyendo CSV:", e)
    return DEFAULT_QUESTIONS.copy()


# UTILIDADES DE DISEÑO

def draw_vertical_gradient(surf, top, bottom):
    h = surf.get_height()
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0]-top[0])*t)
        g = int(top[1] + (bottom[1]-top[1])*t)
        b = int(top[2] + (bottom[2]-top[2])*t)
        pygame.draw.line(surf, (r,g,b), (0,y), (surf.get_width(), y))

def draw_glow_rect(surf, rect, color_rgba, radius=18, layers=6):
    tmp = pygame.Surface((rect.w + layers*2, rect.h + layers*2), pygame.SRCALPHA)
    for i in range(layers, 0, -1):
        alpha = int(color_rgba[3] * (i / layers))
        c = (color_rgba[0], color_rgba[1], color_rgba[2], alpha)
        pygame.draw.rect(tmp, c, pygame.Rect(layers-i, layers-i, rect.w + (i-1)*2, rect.h + (i-1)*2), border_radius=radius)
    surf.blit(tmp, (rect.x - layers, rect.y - layers), special_flags=pygame.BLEND_PREMULTIPLIED)

def rounded_rect(surface, rect, color, radius=14, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius, width=width)


class FancyButton:
    def __init__(self, rect, text, font=FONT_MED):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.hover = False
        self.popping = 0.0
    def draw(self, surf):
        scale = 1.0 - 0.03 * self.popping
        w = int(self.rect.w * scale)
        h = int(self.rect.h * scale)
        x = self.rect.centerx - w//2
        y = self.rect.centery - h//2
        r = pygame.Rect(x,y,w,h)
        if self.hover:
            draw_glow_rect(surf, r, BTN_GLOW, radius=22, layers=7)
        tmp = pygame.Surface((w,h), pygame.SRCALPHA)
        draw_vertical_gradient(tmp, BTN_LEFT, BTN_RIGHT)
        surf.blit(tmp, (x,y))
        pygame.draw.rect(surf, (255,255,255,25), r, border_radius=20, width=2)
        txt = self.font.render(self.text, True, TEXT_BLACK)
        surf.blit(txt, txt.get_rect(center=r.center))
        if self.popping > 0:
            self.popping = max(0.0, self.popping - 0.08)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

    def click_pop(self):
        self.popping = 1.0


class Game:
    def __init__(self):
        self.state = "menu"   # menu, playing, gameover
        self.score = 0
        self.lives = 3
        self.questions = load_questions()
        random.shuffle(self.questions)
        self.qindex = 0
        self.time_per_q = 15
        self.time_left = self.time_per_q
        self.selected = -1
        self.feedback = 0
        self.logo = None
        self.best = self.load_best()
        self.load_assets()
    def load_assets(self):
        if os.path.exists(LOGO_PATH):
            try:
                img = pygame.image.load(LOGO_PATH).convert_alpha()
                w = 160
                h = int(img.get_height() * (w / img.get_width()))
                self.logo = pygame.transform.smoothscale(img, (w,h))
            except:
                self.logo = None
    def load_best(self):
        p = "/mnt/data/best_score.txt"
        try:
            with open(p,"r") as f:
                return int(f.read().strip())
        except:
            return 0
    def save_best(self):
        p = "/mnt/data/best_score.txt"
        try:
            with open(p,"w") as f:
                f.write(str(self.best))
        except:
            pass
    def reset(self):
        self.score = 0
        self.lives = 3
        self.questions = load_questions()
        random.shuffle(self.questions)
        self.qindex = 0
        self.time_left = self.time_per_q
        self.selected = -1
        self.feedback = 0

    def current_q(self):
        if self.qindex < len(self.questions):
            return self.questions[self.qindex]
        return None

    def next_q(self):
        self.qindex += 1
        self.time_left = self.time_per_q
        self.selected = -1


PLAY_BTN = FancyButton((60, 420, 300, 72), "PLAY", FONT_MED)

OPTION_RECTS = [pygame.Rect(40, 360 + i*86, 340, 64) for i in range(4)]


def draw_menu(g: Game):
    draw_vertical_gradient(screen, GRADIENT_TOP, GRADIENT_BOTTOM)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(overlay, (255,255,255,12), (WIDTH//2, 180), 140)
    screen.blit(overlay, (0,0))

    # logo y título
    if g.logo:
        screen.blit(g.logo, g.logo.get_rect(center=(WIDTH//2, 150)))
    else:
        txt = FONT_TITLE.render("¿Sabes o No Sabes", True, TEXT_BLACK)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, 150)))

    mx, my = pygame.mouse.get_pos()
    PLAY_BTN.hover = PLAY_BTN.is_over((mx,my))
    PLAY_BTN.draw(screen)

    pygame.draw.ellipse(screen, (255,220,90), (68, HEIGHT-84, 44, 44))
    ctext = FONT_SMALL.render("1250", True, (30,30,30))
    screen.blit(ctext, ctext.get_rect(center=(90, HEIGHT-62)))

    subt = FONT_SMALL.render("Press PLAY to start", True, TEXT_BLACK)
    screen.blit(subt, (120, 210))


def wrap_text(text, font, maxw):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if font.size(test)[0] <= maxw:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# PANTALLA DE JUEGO
def draw_play(g: Game):
    draw_vertical_gradient(screen, GRADIENT_TOP, GRADIENT_BOTTOM)
    score_txt = FONT_SMALL.render(f"Puntos: {g.score}", True, TEXT_BLACK)
    screen.blit(score_txt, (18, 18))

    for i in range(3):
        x = WIDTH - 24 - i*28
        color = (255,100,100) if i < g.lives else (200,200,200)
        pygame.draw.circle(screen, color, (x, 32), 10)
    # pregunta
    q = g.current_q()
    if not q:
        end = FONT_TITLE.render("¡No hay más preguntas!", True, TEXT_BLACK)
        screen.blit(end, end.get_rect(center=(WIDTH//2, HEIGHT//2)))
        return

    label = FONT_SMALL.render("QUESTION", True, TEXT_BLACK)
    screen.blit(label, (WIDTH//2 - label.get_width()//2, 90))

    lines = wrap_text(q["q"], FONT_MED, WIDTH - 80)
    y0 = 130
    for i, ln in enumerate(lines):
        surf = FONT_MED.render(ln, True, TEXT_BLACK)
        screen.blit(surf, surf.get_rect(center=(WIDTH//2, y0 + i*28)))

    mx, my = pygame.mouse.get_pos()
    for i, rect in enumerate(OPTION_RECTS):
        is_over = rect.collidepoint((mx,my))
        if g.feedback == 0:
            if is_over:
                draw_glow_rect(screen, rect, (140,210,220,70), radius=16, layers=5)
            rounded_rect(screen, rect, (255,255,255,CARD_ALPHA), radius=16)
            txt = FONT_MED.render(q["choices"][i], True, TEXT_BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))
            # si seleccionado con teclado, mostrar borde
            if g.selected == i:
                pygame.draw.rect(screen, ACCENT, rect, width=3, border_radius=16)
        else:
            # feedback: mostrar verde la correcta, rojo la incorrecta seleccionada
            if i == q["answer"]:
                rounded_rect(screen, rect, CORRECT, radius=16)
                txt = FONT_MED.render(q["choices"][i], True, (20,20,20))
                screen.blit(txt, txt.get_rect(center=rect.center))
            else:
                if i == g.selected:
                    rounded_rect(screen, rect, WRONG, radius=16)
                    txt = FONT_MED.render(q["choices"][i], True, (255,255,255))
                    screen.blit(txt, txt.get_rect(center=rect.center))
                else:
                    rounded_rect(screen, rect, (255,255,255,CARD_ALPHA), radius=16)
                    txt = FONT_MED.render(q["choices"][i], True, TEXT_BLACK)
                    screen.blit(txt, txt.get_rect(center=rect.center))
    # barra de tiempo
    bar_w = WIDTH - 80
    x0 = 40
    y_bar = HEIGHT - 120
    pygame.draw.rect(screen, (255,255,255,12), (x0, y_bar, bar_w, 18), border_radius=9)
    pct = max(0, g.time_left / g.time_per_q)
    pygame.draw.rect(screen, ACCENT, (x0, y_bar, int(bar_w * pct), 18), border_radius=9)
    # overlay feedback animado
    if g.feedback != 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        if g.feedback > 0:
            overlay.fill((CORRECT[0], CORRECT[1], CORRECT[2], min(180, int(g.feedback*12))))
        else:
            overlay.fill((WRONG[0], WRONG[1], WRONG[2], min(220, int(-g.feedback*12))))
        screen.blit(overlay, (0,0))


#Comprobar respuesta

def check_answer(g: Game, idx):
    q = g.current_q()
    if not q: return
    if idx == q["answer"]:
        g.score += 10 + int(g.time_left)
        g.feedback = 12
        g.selected = idx
        g.time_left = 0
    else:
        g.lives -= 1
        g.feedback = -14
        g.selected = idx
        g.time_left = 0


def main():
    g = Game()
    play_btn = PLAY_BTN

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if g.state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play_btn.click_pop()
                        g.reset()
                        g.state = "playing"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if play_btn.is_over(pos):
                        play_btn.click_pop()
                        g.reset()
                        g.state = "playing"

            elif g.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        g.selected = (g.selected + 1) % len(OPTION_RECTS)
                    if event.key == pygame.K_UP:
                        g.selected = (g.selected - 1) % len(OPTION_RECTS)
                    if event.key == pygame.K_RETURN and g.selected != -1 and g.feedback == 0:
                        check_answer(g, g.selected)
                    if event.key == pygame.K_ESCAPE:
                        g.state = "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and g.feedback == 0:
                    pos = pygame.mouse.get_pos()
                    for i, r in enumerate(OPTION_RECTS):
                        if r.collidepoint(pos):
                            g.selected = i
                            # animación pop local (draw feedback change)
                            check_answer(g, i)

            elif g.state == "gameover":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        g.reset(); g.state = "playing"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

        # estado por estado
        if g.state == "menu":
            # actualizar botón hover y anim
            mx,my = pygame.mouse.get_pos()
            play_btn.hover = play_btn.is_over((mx,my))
            draw_menu(g)

        elif g.state == "playing":
            # Disminución de tiempo
            if g.feedback == 0:
                g.time_left -= dt
                if g.time_left <= 0:
                    # tiempo agotado: perder vida
                    g.lives -= 1
                    g.feedback = -12
                    g.selected = -1
                    g.time_left = 0
                    if g.lives <= 0:
                        g.state = "gameover"
            else:
                if g.feedback > 0:
                    g.feedback -= 1
                else:
                    g.feedback += 1
                if g.feedback == 0:
                    # avanzar a la siguiente pregunta
                    g.next_q()
                    if g.qindex >= len(g.questions) or g.lives <= 0:
                        if g.score > g.best:
                            g.best = g.score
                            g.save_best()
                        g.state = "gameover"
            draw_play(g)

        elif g.state == "gameover":
            # pantalla de game over
            draw_vertical_gradient(screen, GRADIENT_BOTTOM, GRADIENT_TOP)
            txt = FONT_TITLE.render("Game Over", True, TEXT_BLACK)
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, 180)))
            sc = FONT_MED.render(f"Puntos: {g.score}", True, TEXT_BLACK)
            screen.blit(sc, sc.get_rect(center=(WIDTH//2, 260)))
            hint = FONT_SMALL.render("ENTER para reiniciar  ·  ESC para salir", True, TEXT_BLACK)
            screen.blit(hint, hint.get_rect(center=(WIDTH//2, 340)))

        pygame.display.flip()

if __name__ == "__main__":
    main()
