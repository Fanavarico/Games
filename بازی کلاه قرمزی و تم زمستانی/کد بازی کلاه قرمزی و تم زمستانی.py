import pygame
import random
import sys
import os

# --- تنظیمات کلی بازی ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_HEIGHT = 150  # قد پسر (عرض خودکار تنظیم می‌شود)
SNOWBALL_SIZE = 30
FPS = 60

# رنگ‌ها
WHITE = (255, 255, 255)
RED   = (220, 20, 60)
BLACK = (0, 0, 0)
SNOW  = (240, 248, 255)

# --- مقداردهی اولیه ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snow Dodge - نسخه نهایی")
clock = pygame.time.Clock()
# انتخاب فونت سیستم (Arial)
font_large = pygame.font.SysFont("Arial", 48, bold=True)
font_small = pygame.font.SysFont("Arial", 24, bold=True)

# --- بخش بارگذاری دارایی‌ها (Assets) ---

# ۱. بارگذاری پس‌زمینه
bg_path = "bg.png"
if os.path.exists(bg_path):
    bg_img = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((44, 62, 80))

# ۲. بارگذاری پسر با حفظ تناسب و ایجاد ماسک برای برخورد دقیق
boy_path = "boy.png"
if os.path.exists(boy_path):
    boy_raw = pygame.image.load(boy_path).convert_alpha()
    # محاسبه عرض جدید بر اساس نسبت ابعاد واقعی عکس
    orig_w, orig_h = boy_raw.get_size()
    aspect_ratio = orig_w / orig_h
    player_width = int(PLAYER_HEIGHT * aspect_ratio)
    
    boy_image = pygame.transform.scale(boy_raw, (player_width, PLAYER_HEIGHT))
    boy_mask = pygame.mask.from_surface(boy_image)
else:
    # اگر عکس نبود، یک مستطیل آبی ساده بساز
    player_width = 60
    boy_image = pygame.Surface((player_width, PLAYER_HEIGHT))
    boy_image.fill((50, 150, 255))
    boy_mask = pygame.mask.from_surface(boy_image)

# ۳. ساخت گلوله برف و ماسک آن
snowball_surf = pygame.Surface((SNOWBALL_SIZE, SNOWBALL_SIZE), pygame.SRCALPHA)
pygame.draw.circle(snowball_surf, SNOW, (SNOWBALL_SIZE//2, SNOWBALL_SIZE//2), SNOWBALL_SIZE//2)
snowball_mask = pygame.mask.from_surface(snowball_surf)

# --- توابع کمکی ---

def draw_heart(x, y, size):
    """رسم یک قلب گرافیکی زیبا"""
    pygame.draw.circle(screen, RED, (x - size//4, y), size//4)
    pygame.draw.circle(screen, RED, (x + size//4, y), size//4)
    points = [(x - size//2, y + size//6), (x + size//2, y + size//6), (x, y + size//1.2)]
    pygame.draw.polygon(screen, RED, points)

class Snowball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH - SNOWBALL_SIZE)
        self.y = random.randint(-800, -50)
        self.speed = random.randint(5, 11)

    def fall(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self):
        screen.blit(snowball_surf, (self.x, self.y))

# --- حلقه اصلی بازی ---

def main():
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 30
    hearts = 3
    snowballs = [Snowball() for _ in range(8)]
    game_over = False

    while True:
        # ۱. رسم پس‌زمینه
        screen.blit(background, (0, 0))

        # ۲. مدیریت رویدادها (بستن بازی)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # ۳. حرکت پسر
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= 9
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
                player_x += 9

            # ۴. منطق گلوله‌ها و برخورد دقیق (Mask)
            for ball in snowballs:
                ball.fall()
                ball.draw()
                
                # محاسبه فاصله (Offset) برای چک کردن ماسک‌ها
                offset = (int(ball.x - player_x), int(ball.y - player_y))
                if boy_mask.overlap(snowball_mask, offset):
                    hearts -= 1
                    ball.reset()
                    if hearts <= 0:
                        game_over = True

            # ۵. رسم پسر
            screen.blit(boy_image, (player_x, player_y))

            # ۶. رسم رابط کاربری (قلب‌ها)
            for i in range(hearts):
                draw_heart(40 + (i * 40), 45, 30)
        
        else:
            # --- صفحه Game Over ---
            # تیره کردن پس‌زمینه
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # مختصات Y برای بالاتر آوردن متن
            msg_y = SCREEN_HEIGHT // 2 - 120
            
            # نمایش متن‌ها
            over_text = font_large.render("GAME OVER", True, RED)
            retry_text = font_small.render("Press 'R' to Restart or 'ESC' to Quit", True, WHITE)
            
            screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, msg_y))
            screen.blit(retry_text, (SCREEN_WIDTH//2 - retry_text.get_width()//2, msg_y + 80))
            
            # مدیریت کلیدها در صفحه باخت
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main() # راه اندازی مجدد
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        # ۷. بروزرسانی صفحه
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()