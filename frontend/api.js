// api.js
// 任务3：调用后端 AI 接口并显示结果

// 获取页面元素
const testAiBtn = document.getElementById('testAiBtn');
const aiResult = document.getElementById('aiResult');
const aiResultContent = document.getElementById('aiResultContent');

// 后端接口地址
const API_BASE_URL = 'http://127.0.0.1:8001';

testAiBtn.addEventListener('click', async () => {
    // 显示加载状态
    aiResult.style.display = 'block';
    aiResultContent.textContent = '正在请求 AI 分析接口...';

    try {
        // 发送 GET 请求到后端分析接口
        const response = await fetch(
            `${API_BASE_URL}/ai/analysis/meeting/test_meeting/summary`
        );

        // 检查响应是否成功
        if (!response.ok) {
            throw new Error(`HTTP 错误: ${response.status}`);
        }

        // 解析 JSON 数据
        const data = await response.json();

        // 格式化显示在页面上
        aiResultContent.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        // 请求失败时显示错误提示
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            aiResultContent.textContent = '❌ 请求失败，请确认后端服务已启动。\n\n启动命令：uvicorn main:app --reload --port 8001';
        } else {
            aiResultContent.textContent = `❌ 请求失败：${error.message}`;
        }
    }
});