import random
import string

class CyberPasswordGenerator:
    def __init__(self):
        self.art = """
         ___                  _      ___                      _             
        | _ \__ _ _ _ __ _  _| |_   / __|___ _ _  ___ _ _ __ _| |_ ___ _ _ 
        |  _/ _` | '_/ _| || |  _| | (_ / -_) ' \/ -_) '_/ _` |  _/ _ \ '_|
        |_| \__,_|_| \__|\_,_|\__|  \___\___|_||_\___|_| \__,_|\__\___/_|  
        """
        self.complexity_levels = {
            '1': {'name': 'Basic', 'chars': string.ascii_letters},
            '2': {'name': 'Strong', 'chars': string.ascii_letters + string.digits},
            '3': {'name': 'Fortress', 'chars': string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"},
            '4': {'name': 'Custom', 'sections': 4, 'divider': '-'}
        }
        
    def get_user_input(self):
        print(self.art)
        print("🔒 Password Security Levels 🔒")
        for key, value in self.complexity_levels.items():
            print(f"{key}. {value['name']}")
        
        while True:
            choice = input("\nChoose security level (1-4): ")
            if choice in self.complexity_levels:
                return int(choice)
            print("Invalid choice. Please select 1-4")

    def generate_custom_pattern(self, length):
        section_length = length // 4
        pattern = []
        for _ in range(4):
            chars = random.sample(string.ascii_letters + string.digits + "!@#$%^&*", section_length)
            pattern.append(''.join(chars))
        return self.complexity_levels['4']['divider'].join(pattern)

    def generate_password(self, complexity, length):
        if complexity == 4:
            return self.generate_custom_pattern(length)
        
        chars = self.complexity_levels[str(complexity)]['chars']
        password = []
        
        # Ensure at least one character from each category for non-custom
        if complexity >= 2:
            password.append(random.choice(string.ascii_uppercase))
            password.append(random.choice(string.digits))
        if complexity >= 3:
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill remaining characters
        remaining = length - len(password)
        password += random.choices(chars, k=remaining)
        
        random.shuffle(password)
        return ''.join(password)

    def validate_strength(self, password):
        strength = 0
        if any(c.isupper() for c in password): strength += 1
        if any(c.islower() for c in password): strength += 1
        if any(c.isdigit() for c in password): strength += 1
        if any(c in string.punctuation for c in password): strength += 1
        return min(strength, 4)

    def run(self):
        complexity = self.get_user_input()
        
        while True:
            try:
                length = int(input("\n🔑 Password length (12-32 recommended): "))
                if 8 <= length <= 64:
                    break
                print("Length must be between 8 and 64")
            except ValueError:
                print("Please enter a valid number")
        
        password = self.generate_password(complexity, length)
        strength = self.validate_strength(password)
        
        print("\n" + "="*50)
        print(f"\n✅ Generated Password: \n\n\033[1;36m{password}\033[0m")
        print(f"\n🔋 Password Strength: {'★' * strength} ({strength}/4)")
        print("\n" + "="*50)

if __name__ == "__main__":
    generator = CyberPasswordGenerator()
    generator.run()