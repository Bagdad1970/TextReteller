<template>
  <div class="text-manager">
    <h1 id="main-header">Пересказ текста</h1>
    <div class="text-container">
      <!-- Поле выбора параметров -->
      <div class="params">
        <div class="param_block">
          <label for="max-length">Максимальная длина выходного текста:</label>
          <input
            id="max-length"
            type="number"
            v-model.number="maxLength"
            min="10"
            max="1000"
            step="10"
            placeholder="100"
            :class="{ 'error-border': maxLengthError }"
          />
          <span class="error-message param-error" v-if="maxLengthError">{{ maxLengthError }}</span>
        </div>
        <div class="param_block">
          <label for="correlation">Корреляция (0.0 - 1.0):</label>
          <input
            id="correlation"
            type="number"
            v-model.number="correlation"
            min="0"
            max="1"
            step="0.1"
            placeholder="0.5"
            :class="{ 'error-border': correlationError }"
          />
          <span class="error-message param-error" v-if="correlationError">{{ correlationError }}</span>
        </div>
      </div>

      <!-- Левое поле -->
      <div class="left-panel">
        <h3>Исходный текст</h3>
        <textarea
          v-model="inputText"
          placeholder="Введите текст для сокращения"
          rows="10"
          cols="40"
          :class="{ 'error-border': inputTextError }"
        ></textarea>
        <div class="error-message textarea-error" v-if="inputTextError">{{ inputTextError }}</div>
      </div>

      <!-- Правое поле -->
      <div class="right-panel">
        <h3>Сокращенный текст</h3>
        <div class="button-group">
          <button
            class="mode-button"
            :class="{ 'active-button': activeMode === 'shortened' }"
            @click="setMode('shortened')"
          >
            Экстрактивное сокращение
          </button>
          <button
            class="mode-button"
            :class="{ 'active-button': activeMode === 'retelled' }"
            @click="setMode('retelled')"
          >
            Результат
          </button>
        </div>
        <textarea
          v-model="outputText"
          rows="10"
          cols="40"
        ></textarea>
      </div>
    </div>

    <!-- Кнопка отправки -->
    <button class="submit-button" @click="submitText">Пересказать</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputText: '',
      shortenedText: '',
      retelledText: '',
      maxLength: 100,
      correlation: 0.5,
      activeMode: 'retelled',
      inputTextError: '', // Ошибка для текстового поля
      maxLengthError: '', // Ошибка для maxLength
      correlationError: '', // Ошибка для correlation
    };
  },
  computed: {
    outputText: {
      get() {
        return this.activeMode === 'shortened' ? this.shortenedText : this.retelledText;
      },
      set(value) {
        if (this.activeMode === 'shortened') {
          this.shortenedText = value;
        } else {
          this.retelledText = value;
        }
      },
    },
  },
  methods: {
    setMode(mode) {
      this.activeMode = mode;
      // Сброс всех ошибок при смене режима
      this.inputTextError = '';
      this.maxLengthError = '';
      this.correlationError = '';
    },
    async submitText() {
      // Сброс всех ошибок
      this.inputTextError = '';
      this.maxLengthError = '';
      this.correlationError = '';

      let hasError = false;

      // Валидация inputText
      if (!this.inputText.trim()) {
        this.inputTextError = 'Поле "Исходный текст" не может быть пустым!';
        hasError = true;
      }

      // Валидация correlation
      if (this.correlation === null || this.correlation === '' || this.correlation < 0 || this.correlation > 1) {
        this.correlationError = 'Корреляция должна быть от 0.0 до 1.0';
        hasError = true;
      }

      // Валидация maxLength
      if (this.maxLength === null || this.maxLength === '' || this.maxLength > 1000) {
        this.maxLengthError = 'Максимальная длина не должна быть выше 1000';
        hasError = true;
      }

      if (hasError) {
        return;
      }

      const payload = {
        text: this.inputText,
        max_length: this.maxLength,
        correlation: this.correlation,
      };

      try {
        const response = await axios.post('/api/summarize', payload);
        const { shortened_text, retelled_text } = response.data;

        this.shortenedText = shortened_text || '';
        this.retelledText = retelled_text || '';
      } catch (error) {
        console.error('Ошибка при пересказах текста:', error);
        this.inputTextError = 'Ошибка при пересказе текста. Проверьте, работает ли бэкенд.';
      }
    },
  },
};
</script>

<style scoped>
.text-manager {
  width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
}

#main-header {
  margin-bottom: 10px;
}

.text-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 25px;
}

.param_block {
  display: flex;
  align-items: center;
  gap: 10px; /* Расстояние между элементами */
}

.params {
  display: flex;
  flex-direction: column;
  align-items: left;
  gap: 3px;
  flex-wrap: wrap;
}

.params label {
  font-size: 16px;
  color: #4169e1;
}

.params input {
  padding: 5px;
  font-size: 16px;
  width: 100px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s;
}

.params input.error-border {
  border-color: #ff0000;
  box-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
}

.params input:focus {
  border-color: #4169e1;
  outline: none;
}

.left-panel {
  flex: 1;
}

.left-panel h3 {
  margin-bottom: 10px;
  color: #333;
}

textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  transition: border-color 0.3s;
}

textarea.error-border {
  border-color: #ff0000;
  box-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
}

textarea:focus {
  border-color: #4169e1;
  outline: none;
}

.right-panel {
  flex: 1;
}

.right-panel h3 {
  margin-bottom: 10px;
  color: #333;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.mode-button {
  padding: 8px 16px;
  border: none;
  background: #f0f0f0;
  color: #333;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.3s;
}

.mode-button:hover {
  background: #6be2ff;
}

.mode-button.active-button {
  background: #6be2ff;
  color: #fff;
}

.submit-button {
  padding: 10px 20px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-button:hover {
  background: #218838;
}

.error-message {
  color: #ff0000;
  font-size: 14px;
}

.param-error {
  margin-left: 10px; /* Ошибка параметров отображается слева */
}

.textarea-error {
  margin-top: 5px; /* Ошибка текстового поля отображается снизу */
}
</style>