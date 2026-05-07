// api.js 任务3：调用后端AI测试接口
const testAiBtn = document.getElementById('testAiBtn');
const aiResult = document.getElementById('aiResult');
const aiResultContent = document.getElementById('aiResultContent');

// 接口地址
const AI_TEST_URL = "http://127.0.0.1:8001/ai/analysis/meeting/test/summary";

testAiBtn.addEventListener('click', async () => {
    // 显示结果区域
    aiResult.style.display = 'block';
    aiResultContent.innerText = "正在请求后端接口...";

    try {
        // 发送GET请求
        const res = await fetch(AI_TEST_URL);

        if (!res.ok) {
            throw new Error("接口请求异常，状态码：" + res.status);
        }

        // 解析JSON
        const data = await res.json();
        // 格式化展示JSON
        aiResultContent.innerText = JSON.stringify(data, null, 2);

    } catch (err) {
        console.error("接口调用失败：", err);
        // 后端未启动/跨域/地址错误 友好提示
        aiResultContent.innerText =
`请求失败！
可能原因：
1. 后端服务未启动
2. 接口地址错误
3. 后端跨域未配置
错误信息：${err.message}`;
    }
});
