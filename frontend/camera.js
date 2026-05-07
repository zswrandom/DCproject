// camera.js
// 任务2：摄像头预览功能

// 获取页面元素
const cameraBtn = document.getElementById('cameraBtn');
const localVideo = document.getElementById('localVideo');
const videoPlaceholder = document.getElementById('videoPlaceholder');

// 存储摄像头流，null 表示摄像头未开启
let localStream = null;

cameraBtn.addEventListener('click', async () => {
    // ========== 如果摄像头已开启，则关闭 ==========
    if (localStream) {
        // 停止所有音视频轨道
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;

        // 清空 video 标签
        localVideo.srcObject = null;
        localVideo.style.display = 'none';
        videoPlaceholder.style.display = 'block';

        // 恢复按钮文字
        cameraBtn.textContent = '开启摄像头';
        return;
    }

    // ========== 如果摄像头未开启，则请求权限 ==========
    try {
        // 请求摄像头和麦克风权限（指定 720P 高清）
        localStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: "user"
            },
            audio: true
        });

        // 把流赋值给 video 标签
        localVideo.srcObject = localStream;
        localVideo.style.display = 'block';
        videoPlaceholder.style.display = 'none';

        // 修改按钮文字
        cameraBtn.textContent = '关闭摄像头';
    } catch (error) {
        // 处理错误：用户拒绝权限、设备不存在等
        console.error('获取摄像头失败：', error);

        if (error.name === 'NotAllowedError') {
            alert('摄像头权限被拒绝，请在浏览器设置中允许访问摄像头。');
        } else if (error.name === 'NotFoundError') {
            alert('未检测到摄像头或麦克风设备。');
        } else if (error.name === 'NotReadableError') {
            alert('摄像头被其他应用占用，请关闭其他使用摄像头的程序。');
        } else {
            alert('获取摄像头失败：' + error.message);
        }
    }
});

// 把 localStream 暴露到全局，方便任务4整合时使用
window.localStream = localStream;