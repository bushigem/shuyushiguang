<template>
  <div class="floating-chat">
    <el-button
      type="primary"
      circle
      class="chat-toggle-button"
      @click="toggleChat"
      :icon="ChatDotRound"
    />

    <el-card v-if="isChatOpen" class="chat-window" shadow="always">
      <template #header>
        <div class="chat-header">
          <span>与 AI 助手交流</span>
          <el-button text circle :icon="Close" @click="closeChat" />
        </div>
      </template>

      <div class="chat-messages" ref="messageContainer">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
          <span class="message-content">{{ msg.content }}</span>
        </div>
        <div v-if="isLoading" class="message system">
          <span class="message-content">AI 正在思考中...</span>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="newMessage"
          placeholder="输入你的问题..."
          @keyup.enter="sendMessage"
          clearable
        >
          <template #append>
            <el-button @click="sendMessage" :disabled="!newMessage || isLoading">发送</el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';
import axios from 'axios'; // 假设你使用 axios
import { ElMessage } from 'element-plus';
import { ChatDotRound, Close } from '@element-plus/icons-vue'; // 导入图标

const isChatOpen = ref(false);
const messages = ref([]); // 存储聊天记录 { role: 'user' | 'assistant' | 'system', content: string }
const newMessage = ref('');
const isLoading = ref(false);
const messageContainer = ref(null); // 用于滚动到底部

// --- 配置 API 地址 ---
const API_BASE_URL = 'http://localhost:8000';

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
  if (isChatOpen.value) {
    // 可以添加初始欢迎语
    if (messages.value.length === 0) {
       messages.value.push({ role: 'system', content: '你好！有什么可以帮你的吗？' });
    }
    scrollToBottom();
  }
};

const closeChat = () => {
  isChatOpen.value = false;
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return;

  const userMessage = newMessage.value.trim();
  messages.value.push({ role: 'user', content: userMessage });
  newMessage.value = '';
  isLoading.value = true;
  scrollToBottom();

  try {
    // 修改这里的 URL，在 /api/ 和 /chat/ 之间加上 books/
    const response = await axios.post(`${API_BASE_URL}/api/books/chat/`, { // <--- 修改这里
      message: userMessage,
    });

    if (response.data && response.data.reply) {
      messages.value.push({ role: 'assistant', content: response.data.reply });
    } else {
       messages.value.push({ role: 'system', content: '抱歉，未能获取 AI 回复。' });
    }
  } catch (error) {
    console.error('发送消息失败:', error); // 错误在这里被捕获和打印
    let errorMsg = '发送消息失败，请稍后再试。';
    if (error.response && error.response.data && error.response.data.error) {
        errorMsg = `错误: ${error.response.data.error}`;
    }
    messages.value.push({ role: 'system', content: errorMsg });
    ElMessage.error(errorMsg); // 使用 Element Plus 提示
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};

// 滚动到消息底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};

// 监听消息变化，自动滚动
watch(messages, scrollToBottom, { deep: true });

</script>

<style scoped>
.floating-chat {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000; /* 确保在顶层 */
}

.chat-toggle-button {
  width: 60px;
  height: 60px;
  font-size: 28px; /* 图标大小 */
}

.chat-window {
  position: fixed; /* 改为 fixed 以便定位 */
  bottom: 100px; /* 按钮上方 */
  right: 30px;
  width: 350px;
  height: 500px;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden; /* 防止内容溢出 */
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto; /* 允许消息区域滚动 */
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 15px;
  max-width: 80%;
  word-wrap: break-word; /* 长单词换行 */
}

.message.user {
  background-color: #409EFF;
  color: white;
  margin-left: auto; /* 用户消息靠右 */
  border-bottom-right-radius: 5px;
}

.message.assistant {
  background-color: #e4e6eb;
  color: #333;
  margin-right: auto; /* AI 消息靠左 */
  border-bottom-left-radius: 5px;
}

.message.system {
  font-style: italic;
  color: #999;
  text-align: center;
  font-size: 0.9em;
  background-color: transparent;
}

.message-content {
  display: inline-block; /* 确保背景色包裹内容 */
}

.chat-input {
  padding: 10px;
  border-top: 1px solid #eee;
  background-color: #fff;
}
</style>