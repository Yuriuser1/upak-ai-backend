#!/usr/bin/env python3
"""
Скрипт для управления миграцией UPAK с OpenAI на Yandex GPT

Использование:
    python scripts/migration_control.py --stage 1  # Включить A/B тестирование 50/50
    python scripts/migration_control.py --stage 2  # Перевести 75% на Yandex GPT
    python scripts/migration_control.py --stage 3  # Полная миграция на Yandex GPT
    python scripts/migration_control.py --rollback # Откат на OpenAI
    python scripts/migration_control.py --status   # Текущий статус
"""

import argparse
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings

class MigrationController:
    """Контроллер для управления миграцией"""
    
    def __init__(self):
        self.env_file = Path('.env')
        self.backup_file = Path('.env.backup')
    
    def backup_config(self):
        """Создание резервной копии конфигурации"""
        if self.env_file.exists():
            import shutil
            shutil.copy2(self.env_file, self.backup_file)
            print(f"✅ Создана резервная копия: {self.backup_file}")
    
    def update_env_setting(self, key: str, value: str):
        """Обновление настройки в .env файле"""
        if not self.env_file.exists():
            print(f"❌ Файл {self.env_file} не найден")
            return False
        
        lines = []
        updated = False
        
        with open(self.env_file, 'r') as f:
            for line in f:
                if line.startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    lines.append(line)
        
        if not updated:
            lines.append(f"{key}={value}\n")
        
        with open(self.env_file, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Обновлено: {key}={value}")
        return True
    
    def stage_1_ab_testing(self):
        """ЭТАП 1: Включение A/B тестирования 50/50"""
        print("🚀 ЭТАП 1: Включение A/B тестирования (50% OpenAI, 50% Yandex GPT)")
        self.backup_config()
        
        self.update_env_setting("ENABLE_AB_TESTING", "true")
        self.update_env_setting("YANDEX_GPT_RATIO", "0.5")
        self.update_env_setting("ENABLE_YANDEX_GPT", "true")
        self.update_env_setting("FALLBACK_TO_OPENAI", "true")
        
        print("✅ A/B тестирование включено. Перезапустите приложение.")
    
    def stage_2_increase_yandex(self):
        """ЭТАП 2: Увеличение доли Yandex GPT до 75%"""
        print("🚀 ЭТАП 2: Увеличение доли Yandex GPT до 75%")
        self.backup_config()
        
        self.update_env_setting("ENABLE_AB_TESTING", "true")
        self.update_env_setting("YANDEX_GPT_RATIO", "0.75")
        self.update_env_setting("ENABLE_YANDEX_GPT", "true")
        self.update_env_setting("FALLBACK_TO_OPENAI", "true")
        
        print("✅ Доля Yandex GPT увеличена до 75%. Перезапустите приложение.")
    
    def stage_3_full_migration(self):
        """ЭТАП 3: Полная миграция на Yandex GPT"""
        print("🚀 ЭТАП 3: Полная миграция на Yandex GPT (100%)")
        self.backup_config()
        
        self.update_env_setting("ENABLE_AB_TESTING", "false")
        self.update_env_setting("YANDEX_GPT_RATIO", "1.0")
        self.update_env_setting("ENABLE_YANDEX_GPT", "true")
        self.update_env_setting("FALLBACK_TO_OPENAI", "true")
        
        print("✅ Полная миграция на Yandex GPT завершена. Перезапустите приложение.")
    
    def rollback_to_openai(self):
        """Откат на OpenAI"""
        print("🔄 ОТКАТ: Возврат к OpenAI")
        
        if self.backup_file.exists():
            import shutil
            shutil.copy2(self.backup_file, self.env_file)
            print(f"✅ Конфигурация восстановлена из {self.backup_file}")
        else:
            self.update_env_setting("ENABLE_AB_TESTING", "false")
            self.update_env_setting("YANDEX_GPT_RATIO", "0.0")
            self.update_env_setting("ENABLE_YANDEX_GPT", "false")
            self.update_env_setting("FALLBACK_TO_OPENAI", "true")
            print("✅ Откат к OpenAI выполнен")
        
        print("⚠️  Перезапустите приложение для применения изменений.")
    
    def show_status(self):
        """Показать текущий статус миграции"""
        print("📊 ТЕКУЩИЙ СТАТУС МИГРАЦИИ")
        print("=" * 40)
        
        try:
            from app.core.config import Settings
            current_settings = Settings()
            
            print(f"A/B тестирование: {'✅ Включено' if current_settings.ENABLE_AB_TESTING else '❌ Выключено'}")
            print(f"Yandex GPT включен: {'✅ Да' if current_settings.ENABLE_YANDEX_GPT else '❌ Нет'}")
            print(f"Доля Yandex GPT: {current_settings.YANDEX_GPT_RATIO * 100:.0f}%")
            print(f"Fallback на OpenAI: {'✅ Включен' if current_settings.FALLBACK_TO_OPENAI else '❌ Выключен'}")
            print(f"Yandex credentials: {'✅ Настроены' if current_settings.YANDEX_GPT_API_KEY else '❌ Не настроены'}")
            
            # Определение текущего этапа
            if not current_settings.ENABLE_YANDEX_GPT:
                stage = "Исходное состояние (только OpenAI)"
            elif current_settings.ENABLE_AB_TESTING and current_settings.YANDEX_GPT_RATIO == 0.5:
                stage = "ЭТАП 1: A/B тестирование 50/50"
            elif current_settings.ENABLE_AB_TESTING and current_settings.YANDEX_GPT_RATIO == 0.75:
                stage = "ЭТАП 2: 75% Yandex GPT"
            elif not current_settings.ENABLE_AB_TESTING and current_settings.YANDEX_GPT_RATIO == 1.0:
                stage = "ЭТАП 3: Полная миграция на Yandex GPT"
            else:
                stage = "Кастомная конфигурация"
            
            print(f"\n🎯 Текущий этап: {stage}")
            
        except Exception as e:
            print(f"❌ Ошибка при чтении конфигурации: {e}")

def main():
    parser = argparse.ArgumentParser(description='Управление миграцией UPAK AI Backend')
    parser.add_argument('--stage', type=int, choices=[1, 2, 3], help='Этап миграции (1-3)')
    parser.add_argument('--rollback', action='store_true', help='Откат к OpenAI')
    parser.add_argument('--status', action='store_true', help='Показать текущий статус')
    
    args = parser.parse_args()
    controller = MigrationController()
    
    if args.stage == 1:
        controller.stage_1_ab_testing()
    elif args.stage == 2:
        controller.stage_2_increase_yandex()
    elif args.stage == 3:
        controller.stage_3_full_migration()
    elif args.rollback:
        controller.rollback_to_openai()
    elif args.status:
        controller.show_status()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()