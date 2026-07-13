import pygame
import sys
import os
import json  
import easy, medium, hard, funny, math, double

# --- AUDIO PRE-INIT & SYSTEM BOOT ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()

# --- 📱 DYNAMIC MOBILE SCREEN RESOLUTION ---
info = pygame.display.Info()
if info.current_w > 0 and info.current_h > 0:
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
else:
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 820
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Mega Paheli Universe - Ultimate Keyboard Tuning")

# Colors Theme
BG_COLOR = (15, 23, 42)          
CARD_DEFAULT = (30, 41, 59)      
BORDER_COLOR = (56, 189, 248)    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_CORRECT = (34, 197, 94)    
COLOR_WRONG = (239, 68, 68)      
COLOR_HINT_BTN = (14, 165, 233)   
COLOR_ANS_BTN = (234, 179, 8)     
COLOR_SOUND_BTN = (100, 116, 139) 
TEXT_MUTED = (148, 163, 184)

# 🚀 HALKA FONT BOOST SCALE
scale_factor = (SCREEN_WIDTH / 1100) * 1.12

font_title = pygame.font.SysFont(None, int(75 * scale_factor), bold=True)      
font_card_title = pygame.font.SysFont(None, int(56 * scale_factor), bold=True) 
font_card_stats = pygame.font.SysFont(None, int(32 * scale_factor), bold=True)            
font_body = pygame.font.SysFont(None, int(48 * scale_factor), bold=True)                  
font_feedback = pygame.font.SysFont(None, int(52 * scale_factor), bold=True)   
font_key = pygame.font.SysFont(None, int(38 * scale_factor), bold=True)       

categories_data = {
    "Easy": easy.riddles, "Medium": medium.riddles, "Hard": hard.riddles,
    "Funny": funny.riddles, "Mathematical": math.riddles, "Double Meaning": double.riddles
}
categories = ["Easy", "Medium", "Hard", "Funny", "Mathematical", "Double Meaning"]

# --- 💾 SAVE & LOAD LOGIC ENGINE ---
SAVE_FILE = "progress_data.json"

def load_game_data():
    default_data = {"progress": {cat: 0 for cat in categories}, "sound_on": True}
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                loaded = json.load(f)
                if "progress" in loaded and "sound_on" in loaded:
                    for cat in categories:
                        if cat not in loaded["progress"]: loaded["progress"][cat] = 0
                    return loaded["progress"], loaded["sound_on"]
                else: return loaded, True
        except: return default_data["progress"], default_data["sound_on"]
    return default_data["progress"], default_data["sound_on"]

def save_game_data():
    try:
        with open(SAVE_FILE, "w") as f: json.dump({"progress": player_progress, "sound_on": sound_on}, f)
    except: pass

player_progress, sound_on = load_game_data()

# Sound System Initializer
click_sound, correct_sound, wrong_sound = None, None, None
try:
    pygame.mixer.init()
    if os.path.exists("home_bgm.mp3"):
        pygame.mixer.music.load("home_bgm.mp3")
        pygame.mixer.music.set_volume(0.20 if sound_on else 0.0)
        pygame.mixer.music.play(-1)
    if os.path.exists("hover.mp3"): 
        click_sound = pygame.mixer.Sound("hover.mp3"); click_sound.set_volume(0.6 if sound_on else 0.0)
    if os.path.exists("correct.mp3"): 
        correct_sound = pygame.mixer.Sound("correct.mp3"); correct_sound.set_volume(0.8 if sound_on else 0.0)
    if os.path.exists("wrong.mp3"): 
        wrong_sound = pygame.mixer.Sound("wrong.mp3"); wrong_sound.set_volume(0.8 if sound_on else 0.0)
except: pass

def update_sound_volumes():
    if sound_on:
        pygame.mixer.music.set_volume(0.20)
        if click_sound: click_sound.set_volume(0.6)
        if correct_sound: correct_sound.set_volume(0.8)
        if wrong_sound: wrong_sound.set_volume(0.8)
    else:
        pygame.mixer.music.set_volume(0.0)
        if click_sound: click_sound.set_volume(0.0)
        if correct_sound: correct_sound.set_volume(0.0)
        if wrong_sound: wrong_sound.set_volume(0.0)

def draw_text_wrapped(surface, text, font, color, rect):
    words = text.split(' ')
    space = font.size(' ')[0]
    x, y = rect.x + 25, rect.y + 25
    max_width = rect.width - 50
    for word in words:
        word_surface = font.render(word, True, color)
        if x + word_surface.get_width() >= rect.x + max_width:
            x = rect.x + 25; y += word_surface.get_height() + 6
        surface.blit(word_surface, (x, y)); x += word_surface.get_width() + space

# Keyboard Layout Configuration
keys_layout = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "←"],
    ["CLR", "z", "x", "c", "SPACE", "v", "b", "n", "m", "OK"]
]
keyboard_rects = {}

def draw_mobile_keyboard():
    keyboard_rects.clear()
    button_size = int(68 * (SCREEN_WIDTH / 1100))
    gap = int(8 * (SCREEN_WIDTH / 1100))
    # 🚀 KEYBOARD KO CORNER SE AUR UPAR SHIFT KIYA (135 pixel clear spacing from bottom)
    start_y = SCREEN_HEIGHT - (3 * (button_size + gap)) - int(135 * (SCREEN_HEIGHT / 820))
    
    for row_idx, row in enumerate(keys_layout):
        total_width = sum([button_size*2 if c=="SPACE" else int(button_size*1.3) if c in ["CLR","OK"] else button_size for c in row]) + (len(row)-1)*gap
        curr_x = (SCREEN_WIDTH - total_width) // 2
        for char in row:
            w = button_size*2 if char=="SPACE" else int(button_size*1.3) if char in ["CLR","OK"] else button_size
            rect = pygame.Rect(curr_x, start_y + row_idx*(button_size+gap), w, button_size)
            keyboard_rects[char] = rect
            btn_col = (185, 28, 28) if char=="CLR" else (34, 197, 94) if char=="OK" else (71, 85, 105) if char in ["←","SPACE"] else (241, 245, 249)
            text_col = WHITE if btn_col != (241, 245, 249) else BLACK
            pygame.draw.rect(screen, btn_col, rect, 0, int(8 * (SCREEN_WIDTH / 1100)))
            pygame.draw.rect(screen, BORDER_COLOR, rect, 2, int(8 * (SCREEN_WIDTH / 1100)))
            surf = font_key.render(char, True, text_col)
            screen.blit(surf, surf.get_rect(center=rect.center))
            curr_x += w + gap

# Engine Flags
current_screen, selected_category, user_input, feedback_text, feedback_timer = "MENU", categories[0], "", "", 0
current_feedback_color = COLOR_CORRECT
clock = pygame.time.Clock()

# Dual Ad Simulation Flags
ad_screen_active = False
ad_timer = 0
ad_type = ""  
target_answer = ""

while True:
    screen.fill(BG_COLOR)
    dt = clock.tick(60)
    
    # Ad Screen Overlay Logic
    if ad_screen_active:
        ad_timer -= dt
        if ad_timer <= 0:
            ad_screen_active = False
            if ad_type == "HINT":
                if len(target_answer) > 2:
                    hint_msg = target_answer[0] + " _ " * (len(target_answer)-2) + target_answer[-1]
                else: hint_msg = target_answer[0] + " _"
                feedback_text = f"Hint: {hint_msg.upper()}"
                current_feedback_color = COLOR_HINT_BTN; feedback_timer = 7000  
            elif ad_type == "ANSWER":
                feedback_text = f"Answer: {target_answer.upper()}"
                current_feedback_color = COLOR_ANS_BTN; feedback_timer = 7000
        
        screen.fill((10, 15, 30))
        ad_title_text = "PLAYING 10s SHORT AD..." if ad_type == "HINT" else "PLAYING 30s REWARD VIDEO..."
        ad_color = COLOR_HINT_BTN if ad_type == "HINT" else COLOR_ANS_BTN
        
        ad_title = font_title.render(ad_title_text, True, ad_color)
        screen.blit(ad_title, ad_title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
        
        seconds_left = max(1, int(ad_timer / 1000) + 1)
        timer_text = font_body.render(f"Remaining Time: {seconds_left} sec", True, WHITE)
        screen.blit(timer_text, timer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))
        
        pygame.display.flip()
        continue

    if feedback_timer > 0:
        feedback_timer -= dt
        if feedback_timer <= 0: feedback_text = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            
            if current_screen == "MENU":
                # Sound Box Collision
                sound_btn_rect = pygame.Rect(SCREEN_WIDTH - int(250 * (SCREEN_WIDTH / 1100)), 40, int(190 * (SCREEN_WIDTH / 1100)), int(65 * (SCREEN_WIDTH / 1100)))
                if sound_btn_rect.collidepoint(pos):
                    sound_on = not sound_on; update_sound_volumes(); save_game_data()
                    if sound_on and click_sound: click_sound.play()
                
                for i, cat in enumerate(categories):
                    rect = pygame.Rect(80, int(180 * (SCREEN_WIDTH / 1100)) + i * int(105 * (SCREEN_WIDTH / 1100)), SCREEN_WIDTH - 160, int(90 * (SCREEN_WIDTH / 1100)))
                    if rect.collidepoint(pos):
                        if click_sound: click_sound.play()
                        selected_category = cat; current_screen = "GAMEPLAY"; user_input = ""; feedback_text = ""
                        
            elif current_screen == "GAMEPLAY":
                if pygame.Rect(30, 25, int(240 * (SCREEN_WIDTH / 1100)), int(70 * (SCREEN_WIDTH / 1100))).collidepoint(pos):
                    if click_sound: click_sound.play()
                    current_screen = "MENU"
                
                # Dynamic Coordinates Grid for Buttons
                hint_rect = pygame.Rect(SCREEN_WIDTH - int(400 * (SCREEN_WIDTH / 1100)), int(340 * (SCREEN_WIDTH / 1100)), int(170 * (SCREEN_WIDTH / 1100)), int(80 * (SCREEN_WIDTH / 1100)))
                ans_rect = pygame.Rect(SCREEN_WIDTH - int(210 * (SCREEN_WIDTH / 1100)), int(340 * (SCREEN_WIDTH / 1100)), int(170 * (SCREEN_WIDTH / 1100)), int(80 * (SCREEN_WIDTH / 1100)))
                idx = player_progress[selected_category]
                
                if idx < len(categories_data[selected_category]):
                    if hint_rect.collidepoint(pos):
                        if click_sound: click_sound.play()
                        ad_screen_active = True; ad_timer = 10000; ad_type = "HINT"
                        target_answer = categories_data[selected_category][idx]["answer"]
                    elif ans_rect.collidepoint(pos):
                        if click_sound: click_sound.play()
                        ad_screen_active = True; ad_timer = 30000; ad_type = "ANSWER"
                        target_answer = categories_data[selected_category][idx]["answer"]
                    
                for char, rect in keyboard_rects.items():
                    if rect.collidepoint(pos):
                        if click_sound: click_sound.play()
                        if char == "←": user_input = user_input[:-1]
                        elif char == "CLR": user_input = ""
                        elif char == "SPACE": user_input += " "
                        elif char == "OK":
                            ans = user_input.strip().lower()
                            if idx < len(categories_data[selected_category]):
                                if ans == categories_data[selected_category][idx]["answer"].lower():
                                    feedback_text = "✓ Sahi Jawab!"
                                    current_feedback_color = COLOR_CORRECT; player_progress[selected_category] += 1; user_input = ""; save_game_data()  
                                    if correct_sound: correct_sound.play()
                                else: 
                                    feedback_text = "✗ Galat Jawab!"
                                    current_feedback_color = COLOR_WRONG
                                    if wrong_sound: wrong_sound.play()
                                feedback_timer = 2000
                        elif len(user_input) < 25: user_input += char

    if current_screen == "MENU":
        title = font_title.render("MEGA PAHELI UNIVERSE", True, BORDER_COLOR)
        screen.blit(title, (80, 40))
        
        # Draw Sound Toggle Button
        sound_btn_rect = pygame.Rect(SCREEN_WIDTH - int(250 * (SCREEN_WIDTH / 1100)), 40, int(190 * (SCREEN_WIDTH / 1100)), int(65 * (SCREEN_WIDTH / 1100)))
        pygame.draw.rect(screen, COLOR_SOUND_BTN, sound_btn_rect, 0, 12); pygame.draw.rect(screen, WHITE, sound_btn_rect, 2, 12)
        sound_label = "SOUND: ON" if sound_on else "SOUND: OFF"
        lbl_surf = font_card_stats.render(sound_label, True, WHITE)
        screen.blit(lbl_surf, lbl_surf.get_rect(center=sound_btn_rect.center))
        
        for i, cat in enumerate(categories):
            rect = pygame.Rect(80, int(180 * (SCREEN_WIDTH / 1100)) + i * int(105 * (SCREEN_WIDTH / 1100)), SCREEN_WIDTH - 160, int(90 * (SCREEN_WIDTH / 1100)))
            pygame.draw.rect(screen, CARD_DEFAULT, rect, 0, 14); pygame.draw.rect(screen, BORDER_COLOR, rect, 2, 14)
            screen.blit(font_card_title.render(cat, True, WHITE), (rect.x + 40, rect.y + int(10 * scale_factor)))
            screen.blit(font_card_stats.render(f"Solved: {player_progress[cat]} / {len(categories_data[cat])}", True, TEXT_MUTED), (rect.x + 40, rect.y + int(52 * (SCREEN_WIDTH / 1100))))

    elif current_screen == "GAMEPLAY":
        back = pygame.Rect(30, 25, int(240 * (SCREEN_WIDTH / 1100)), int(70 * (SCREEN_WIDTH / 1100)))
        pygame.draw.rect(screen, CARD_DEFAULT, back, 0, 12); pygame.draw.rect(screen, BORDER_COLOR, back, 2, 12)
        screen.blit(font_card_stats.render("< Back to Menu", True, WHITE), (back.x + 25, back.y + int(18 * (SCREEN_WIDTH / 1100))))
        
        idx = player_progress[selected_category]
        if idx < len(categories_data[selected_category]):
            # Balanced Riddle Box
            box = pygame.Rect(80, int(140 * (SCREEN_WIDTH / 1100)), SCREEN_WIDTH - 160, int(170 * (SCREEN_WIDTH / 1100)))
            pygame.draw.rect(screen, CARD_DEFAULT, box, 0, 18); pygame.draw.rect(screen, BORDER_COLOR, box, 3, 18)
            draw_text_wrapped(screen, categories_data[selected_category][idx]["riddle"], font_body, WHITE, box)
            
            # Balanced Input Box
            in_box = pygame.Rect(80, int(340 * (SCREEN_WIDTH / 1100)), SCREEN_WIDTH - int(500 * (SCREEN_WIDTH / 1100)), int(80 * (SCREEN_WIDTH / 1100)))
            pygame.draw.rect(screen, WHITE, in_box, 0, 12); pygame.draw.rect(screen, BORDER_COLOR, in_box, 2, 12)
            screen.blit(font_body.render(user_input, True, BLACK), (in_box.x + 30, in_box.y + int(16 * (SCREEN_WIDTH / 1100))))
            
            # Balanced HINT Button
            hint_btn = pygame.Rect(SCREEN_WIDTH - int(400 * (SCREEN_WIDTH / 1100)), int(340 * (SCREEN_WIDTH / 1100)), int(170 * (SCREEN_WIDTH / 1100)), int(80 * (SCREEN_WIDTH / 1100)))
            pygame.draw.rect(screen, COLOR_HINT_BTN, hint_btn, 0, 12); pygame.draw.rect(screen, WHITE, hint_btn, 2, 12)
            lbl = font_card_stats.render("HINT 10s", True, WHITE)
            screen.blit(lbl, lbl.get_rect(center=hint_btn.center))
            
            # Balanced ANSWER Button
            ans_btn = pygame.Rect(SCREEN_WIDTH - int(210 * (SCREEN_WIDTH / 1100)), int(340 * (SCREEN_WIDTH / 1100)), int(170 * (SCREEN_WIDTH / 1100)), int(80 * (SCREEN_WIDTH / 1100)))
            pygame.draw.rect(screen, COLOR_ANS_BTN, ans_btn, 0, 12); pygame.draw.rect(screen, WHITE, ans_btn, 2, 12)
            lbl = font_card_stats.render("ANS 30s", True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=ans_btn.center))
            
            if feedback_text: 
                screen.blit(font_feedback.render(feedback_text, True, current_feedback_color), (80, int(450 * (SCREEN_WIDTH / 1100))))
            draw_mobile_keyboard()
        else:
            victory_txt = font_title.render("CONGRATULATIONS!", True, COLOR_CORRECT)
            screen.blit(victory_txt, victory_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3)))
            draw_mobile_keyboard()

    pygame.display.flip()
