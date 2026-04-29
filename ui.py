import langomizer as lm
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# Color scheme
BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#3498db"
SECONDARY_COLOR = "#2ecc71"
ERROR_COLOR = "#e74c3c"
SUCCESS_COLOR = "#27ae60"
LABEL_COLOR = "#ecf0f1"

class LangomizerUi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Langomizer - Language Generator")
        self.geometry("700x850")
        self.configure(bg=BG_COLOR)
        
        # Configure style
        self.setup_styles()
        
        # Main container with notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.translator_frame = ttk.Frame(self.notebook)
        self.examples_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.translator_frame, text="Translator")
        self.notebook.add(self.examples_frame, text="Examples")
        self.notebook.add(self.settings_frame, text="Settings & Grammar")
        
        # Initialize components
        self.setup_translator_tab()
        self.setup_examples_tab()
        self.setup_settings_tab()
        
        self.vowels = ['a', 'e', 'i', 'o', 'u']
        self.consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
        self.lang = None
        self.used_seed = None
        self.translation_history = []
        
        # Example words for different categories
        self.example_words = {
            'noun': ['cat', 'house', 'tree', 'water', 'mountain', 'friend', 'book'],
            'verb': ['run', 'eat', 'sleep', 'jump', 'talk', 'write', 'sing'],
            'adjective': ['red', 'big', 'happy', 'cold', 'soft', 'brave', 'quiet'],
            'preposition': ['in', 'on', 'at', 'by', 'from', 'with'],
            'pronoun': ['I', 'you', 'he', 'she', 'it', 'we', 'they'],
            'conjunction': ['and', 'or', 'but', 'nor'],
        }

    def setup_styles(self):
        """Configure ttk styles for the entire application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for all widgets
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR)
        style.configure('TButton', font=('Helvetica', 10))
        style.map('TButton',
                  background=[('active', ACCENT_COLOR)],
                  foreground=[('active', FG_COLOR)])
        style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])

    def setup_translator_tab(self):
        """Create the main translator tab"""
        main_frame = ttk.Frame(self.translator_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(main_frame, text="Word Translator", 
                              font=('Helvetica', 16, 'bold'),
                              bg=BG_COLOR, fg=ACCENT_COLOR)
        title_label.pack(pady=(0, 15))
        
        # Seed section
        seed_frame = ttk.LabelFrame(main_frame, text="Language Configuration")
        seed_frame.pack(fill=tk.X, pady=(0, 15))
        
        seed_label = ttk.Label(seed_frame, text="Enter seed (for consistent language):")
        seed_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.number_entry = tk.Entry(seed_frame, font=('Helvetica', 11), 
                                     width=20, bg="#3a3a3a", fg=FG_COLOR,
                                     insertbackground=ACCENT_COLOR)
        self.number_entry.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Translation Input")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        text_label = ttk.Label(input_frame, text="Enter word:")
        text_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.text_entry = tk.Entry(input_frame, font=('Helvetica', 11),
                                   bg="#3a3a3a", fg=FG_COLOR,
                                   insertbackground=ACCENT_COLOR)
        self.text_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        word_type_label = ttk.Label(input_frame, text="Choose word type:")
        word_type_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        self.dropdown_var = tk.StringVar(value="noun")
        self.dropdown = ttk.Combobox(input_frame, textvariable=self.dropdown_var,
                                     values=("noun", "verb", "adjective", 
                                            "conjunction", "pronoun", "preposition"),
                                     state="readonly", width=30)
        self.dropdown.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        translate_btn = tk.Button(button_frame, text="Translate",
                                 command=self.handle_submit,
                                 bg=ACCENT_COLOR, fg=FG_COLOR,
                                 font=('Helvetica', 11, 'bold'),
                                 padx=15, pady=8)
        translate_btn.pack(side=tk.LEFT, padx=5)
        
        random_btn = tk.Button(button_frame, text="Random Example",
                              command=self.translate_random_example,
                              bg=SECONDARY_COLOR, fg=FG_COLOR,
                              font=('Helvetica', 11, 'bold'),
                              padx=15, pady=8)
        random_btn.pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Translation Result")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.output_label = tk.Label(output_frame, text="Enter a word and click 'Translate'",
                                    font=('Helvetica', 12, 'bold'),
                                    bg="#3a3a3a", fg=SECONDARY_COLOR,
                                    wraplength=600, justify=tk.CENTER,
                                    padx=15, pady=30)
        self.output_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # History section
        history_frame = ttk.LabelFrame(main_frame, text="Translation History")
        history_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.history_label = tk.Label(history_frame, text="No translations yet",
                                     font=('Helvetica', 9),
                                     bg="#3a3a3a", fg="#bdc3c7",
                                     wraplength=550, justify=tk.LEFT,
                                     padx=10, pady=10)
        self.history_label.pack(fill=tk.X, padx=10, pady=10)

    def setup_examples_tab(self):
        """Create the examples and grammar tab"""
        main_frame = ttk.Frame(self.examples_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_label = tk.Label(main_frame, text="Language Examples & Grammar",
                              font=('Helvetica', 16, 'bold'),
                              bg=BG_COLOR, fg=ACCENT_COLOR)
        title_label.pack(pady=(0, 15))
        
        # Seed entry for examples
        seed_frame = ttk.Frame(main_frame)
        seed_frame.pack(fill=tk.X, pady=(0, 15))
        
        seed_label = ttk.Label(seed_frame, text="Enter seed to generate examples:")
        seed_label.pack(side=tk.LEFT, padx=5)
        
        self.examples_seed_entry = tk.Entry(seed_frame, font=('Helvetica', 10),
                                           width=15, bg="#3a3a3a", fg=FG_COLOR,
                                           insertbackground=ACCENT_COLOR)
        self.examples_seed_entry.pack(side=tk.LEFT, padx=5)
        
        generate_btn = tk.Button(seed_frame, text="Generate",
                                command=self.show_all_examples,
                                bg=ACCENT_COLOR, fg=FG_COLOR,
                                font=('Helvetica', 10, 'bold'),
                                padx=10, pady=5)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Examples display
        self.examples_text = scrolledtext.ScrolledText(main_frame, height=30,
                                                       font=('Courier', 10),
                                                       bg="#3a3a3a", fg=SECONDARY_COLOR,
                                                       insertbackground=ACCENT_COLOR)
        self.examples_text.pack(fill=tk.BOTH, expand=True)
        
        placeholder = """Generate examples by entering a seed number above.

Examples will show translations for:
• Common nouns (cat, house, tree, water, etc.)
• Verbs (run, eat, sleep, jump, etc.)
• Adjectives (red, big, happy, cold, etc.)
• And more!

Plus a detailed breakdown of grammar rules for your language."""
        
        self.examples_text.insert('1.0', placeholder)
        self.examples_text.config(state=tk.DISABLED)

    def setup_settings_tab(self):
        """Create the settings and grammar tab"""
        main_frame = ttk.Frame(self.settings_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_label = tk.Label(main_frame, text="Settings & Grammar Rules",
                              font=('Helvetica', 16, 'bold'),
                              bg=BG_COLOR, fg=ACCENT_COLOR)
        title_label.pack(pady=(0, 15))
        
        # Letter customization
        letter_frame = ttk.LabelFrame(main_frame, text="Customize Letters")
        letter_frame.pack(fill=tk.X, pady=(0, 15))
        
        edit_btn = tk.Button(letter_frame, text="Edit Letters",
                            command=self.open_letter_edit,
                            bg=SECONDARY_COLOR, fg=FG_COLOR,
                            font=('Helvetica', 11, 'bold'),
                            padx=15, pady=8)
        edit_btn.pack(padx=10, pady=10)
        
        # Grammar display
        grammar_frame = ttk.LabelFrame(main_frame, text="Language Grammar Rules")
        grammar_frame.pack(fill=tk.BOTH, expand=True)
        
        seed_label = ttk.Label(grammar_frame, text="Enter seed to show grammar:")
        seed_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        grammar_seed_frame = ttk.Frame(grammar_frame)
        grammar_seed_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.grammar_seed_entry = tk.Entry(grammar_seed_frame, font=('Helvetica', 10),
                                          width=15, bg="#3a3a3a", fg=FG_COLOR,
                                          insertbackground=ACCENT_COLOR)
        self.grammar_seed_entry.pack(side=tk.LEFT, padx=5)
        
        grammar_btn = tk.Button(grammar_seed_frame, text="Show Grammar",
                               command=self.show_grammar,
                               bg=ACCENT_COLOR, fg=FG_COLOR,
                               font=('Helvetica', 10, 'bold'),
                               padx=10, pady=5)
        grammar_btn.pack(side=tk.LEFT, padx=5)
        
        self.grammar_text = scrolledtext.ScrolledText(grammar_frame, height=20,
                                                      font=('Courier', 10),
                                                      bg="#3a3a3a", fg=SECONDARY_COLOR,
                                                      insertbackground=ACCENT_COLOR)
        self.grammar_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        placeholder = "Enter a seed number above and click 'Show Grammar' to see the language rules."
        self.grammar_text.insert('1.0', placeholder)
        self.grammar_text.config(state=tk.DISABLED)

    def handle_submit(self):
        """Handle word translation"""
        text = self.text_entry.get().strip()
        seed_str = self.number_entry.get().strip()
        option = self.dropdown_var.get()
        
        if not seed_str:
            self.output_label.config(text="Please enter a seed", fg=ERROR_COLOR)
            return
        
        try:
            self.used_seed = int(seed_str)
        except ValueError:
            self.output_label.config(text="Invalid seed - must be a number", fg=ERROR_COLOR)
            return
        
        if not text:
            self.output_label.config(text="Please enter a word", fg=ERROR_COLOR)
            return
        
        self.lang = lm.SimpleLanguage(seed=self.used_seed, consonants=self.consonants, 
                                     vowels=self.vowels)
        translation = self.lang.translate(text, option)
        
        self.output_label.config(text=f"'{text}' ({option}) → '{translation}'", 
                                fg=SUCCESS_COLOR)
        
        # Add to history
        self.translation_history.insert(0, f"'{text}' → '{translation}'")
        self.translation_history = self.translation_history[:10]
        self.update_history_display()

    def translate_random_example(self):
        """Translate a random example word"""
        import random
        word_type = self.dropdown_var.get()
        if word_type in self.example_words:
            random_word = random.choice(self.example_words[word_type])
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, random_word)
            self.handle_submit()

    def update_history_display(self):
        """Update the translation history display"""
        if self.translation_history:
            history_text = " | ".join(self.translation_history)
            self.history_label.config(text=history_text)
        else:
            self.history_label.config(text="No translations yet")

    def show_all_examples(self):
        """Generate and show all examples for the language"""
        seed_str = self.examples_seed_entry.get().strip()
        
        if not seed_str:
            self.examples_text.config(state=tk.NORMAL)
            self.examples_text.delete('1.0', tk.END)
            self.examples_text.insert('1.0', "Please enter a seed number")
            self.examples_text.config(state=tk.DISABLED)
            return
        
        try:
            seed = int(seed_str)
        except ValueError:
            self.examples_text.config(state=tk.NORMAL)
            self.examples_text.delete('1.0', tk.END)
            self.examples_text.insert('1.0', "Invalid seed - must be a number")
            self.examples_text.config(state=tk.DISABLED)
            return
        
        lang = lm.SimpleLanguage(seed=seed, consonants=self.consonants, 
                               vowels=self.vowels)
        
        examples_text = f"Language Examples (Seed: {seed})\n"
        examples_text += "=" * 60 + "\n\n"
        
        for word_type, words in self.example_words.items():
            examples_text += f"{word_type.upper()}S:\n"
            translations = []
            for word in words:
                translation = lang.translate(word, word_type)
                translations.append(f"  {word:15} → {translation}")
            examples_text += "\n".join(translations)
            examples_text += "\n\n"
        
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete('1.0', tk.END)
        self.examples_text.insert('1.0', examples_text)
        self.examples_text.config(state=tk.DISABLED)

    def show_grammar(self):
        """Show grammar rules for the language"""
        seed_str = self.grammar_seed_entry.get().strip()
        
        if not seed_str:
            self.grammar_text.config(state=tk.NORMAL)
            self.grammar_text.delete('1.0', tk.END)
            self.grammar_text.insert('1.0', "Please enter a seed number")
            self.grammar_text.config(state=tk.DISABLED)
            return
        
        try:
            seed = int(seed_str)
        except ValueError:
            self.grammar_text.config(state=tk.NORMAL)
            self.grammar_text.delete('1.0', tk.END)
            self.grammar_text.insert('1.0', "Invalid seed - must be a number")
            self.grammar_text.config(state=tk.DISABLED)
            return
        
        lang = lm.SimpleLanguage(seed=seed, consonants=self.consonants, 
                               vowels=self.vowels)
        
        grammar = lang.describe_grammar_basics()
        
        self.grammar_text.config(state=tk.NORMAL)
        self.grammar_text.delete('1.0', tk.END)
        self.grammar_text.insert('1.0', grammar)
        self.grammar_text.config(state=tk.DISABLED)

    def open_letter_edit(self):
        """Open letter customization window"""
        vowels = ['a', 'e', 'i', 'o', 'u']
        consonants = [
            'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q',
            'r', 's', 't', 'v', 'w', 'x', 'y', 'z'
        ]

        window = tk.Toplevel(self)
        window.title("Select Letters")
        window.geometry("600x500")
        window.configure(bg=BG_COLOR)

        title = tk.Label(window, text="Customize Language Letters",
                        font=('Helvetica', 14, 'bold'),
                        bg=BG_COLOR, fg=ACCENT_COLOR)
        title.pack(pady=10)

        vowel_label = tk.Label(window, text="Vowels", font=('Helvetica', 12, 'bold'),
                              bg=BG_COLOR, fg=LABEL_COLOR)
        vowel_label.pack(anchor=tk.W, padx=15, pady=(10, 5))

        vowel_frame = tk.Frame(window, bg=BG_COLOR)
        vowel_frame.pack(padx=15)

        vowel_vars = []
        for idx, v in enumerate(vowels):
            var = tk.BooleanVar(value=True if v in self.vowels else False)
            cb = tk.Checkbutton(vowel_frame, text=v, variable=var,
                              bg=BG_COLOR, fg=FG_COLOR, 
                              selectcolor="#3a3a3a", activebackground=BG_COLOR)
            cb.grid(row=idx//5, column=idx%5, sticky='w', padx=5, pady=2)
            vowel_vars.append((v, var))

        consonant_label = tk.Label(window, text="Consonants", 
                                  font=('Helvetica', 12, 'bold'),
                                  bg=BG_COLOR, fg=LABEL_COLOR)
        consonant_label.pack(anchor=tk.W, padx=15, pady=(15, 5))

        consonant_frame = tk.Frame(window, bg=BG_COLOR)
        consonant_frame.pack(padx=15)

        consonant_vars = []
        for idx, c in enumerate(consonants):
            var = tk.BooleanVar(value=True if c in self.consonants else False)
            cb = tk.Checkbutton(consonant_frame, text=c, variable=var,
                              bg=BG_COLOR, fg=FG_COLOR,
                              selectcolor="#3a3a3a", activebackground=BG_COLOR)
            cb.grid(row=idx//5, column=idx%5, sticky='w', padx=5, pady=2)
            consonant_vars.append((c, var))

        def select_all():
            for _, var in vowel_vars + consonant_vars:
                var.set(True)

        def deselect_all():
            for _, var in vowel_vars + consonant_vars:
                var.set(False)

        def get_selected():
            selected_vowels = [v for v, var in vowel_vars if var.get()]
            selected_consonants = [c for c, var in consonant_vars if var.get()]
            if len(selected_vowels) > 0 and len(selected_consonants) > 0:
                self.vowels = selected_vowels
                self.consonants = selected_consonants
                window.destroy()
            else:
                error_window = tk.Toplevel(window)
                error_window.title("Error")
                error_window.configure(bg=BG_COLOR)
                text = "You need to select at least one vowel and one consonant."
                label = tk.Label(error_window, text=text, wraplength=300, 
                               justify="left", bg=BG_COLOR, fg=ERROR_COLOR,
                               font=('Helvetica', 10))
                label.pack(padx=10, pady=10)
                close_button = tk.Button(error_window, text="Close",
                                       command=error_window.destroy,
                                       bg=ERROR_COLOR, fg=FG_COLOR)
                close_button.pack(pady=10)

        button_frame = tk.Frame(window, bg=BG_COLOR)
        button_frame.pack(pady=15)

        select_all_button = tk.Button(button_frame, text="Select All",
                                     command=select_all,
                                     bg=SECONDARY_COLOR, fg=FG_COLOR,
                                     font=('Helvetica', 10, 'bold'),
                                     padx=10, pady=5)
        select_all_button.grid(row=0, column=0, padx=5)

        deselect_all_button = tk.Button(button_frame, text="Deselect All",
                                       command=deselect_all,
                                       bg=ERROR_COLOR, fg=FG_COLOR,
                                       font=('Helvetica', 10, 'bold'),
                                       padx=10, pady=5)
        deselect_all_button.grid(row=0, column=1, padx=5)

        submit_button = tk.Button(window, text="Apply Settings",
                                 command=get_selected,
                                 bg=ACCENT_COLOR, fg=FG_COLOR,
                                 font=('Helvetica', 11, 'bold'),
                                 padx=15, pady=8)
        submit_button.pack(pady=10)


if __name__ == "__main__":
    app = LangomizerUi()
    app.mainloop()
