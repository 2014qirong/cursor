/**
 * 图片压缩工具
 * 功能包括：
 * - 拖放或选择文件上传
 * - 调整压缩质量
 * - 调整输出格式
 * - 调整图片尺寸
 * - 压缩前后对比预览
 */

document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const compressionInterface = document.getElementById('compressionInterface');
    const previewContainer = document.getElementById('previewContainer');
    const compressBtn = document.getElementById('compressBtn');
    const resetBtn = document.getElementById('resetBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const comparisonView = document.getElementById('comparisonView');
    const comparisonContainer = document.getElementById('comparisonContainer');
    const comparisonImage = document.getElementById('comparisonImage');
    const comparisonOriginal = document.getElementById('comparisonOriginal');
    const comparisonCompressed = document.getElementById('comparisonCompressed');
    const comparisonSlider = document.getElementById('comparisonSlider');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsList = document.getElementById('resultsList');
    const downloadAllBtn = document.getElementById('downloadAllBtn');
    
    // 压缩选项
    const qualitySlider = document.getElementById('qualitySlider');
    const qualityValue = document.getElementById('qualityValue');
    const formatSelect = document.getElementById('formatSelect');
    const resizeCheckbox = document.getElementById('resizeCheckbox');
    const resizeOptions = document.getElementById('resizeOptions');
    const widthInput = document.getElementById('widthInput');
    const heightInput = document.getElementById('heightInput');
    const aspectRatioCheckbox = document.getElementById('aspectRatioCheckbox');
    
    // 存储原始文件和压缩后的文件
    let originalFiles = [];
    let processedFiles = [];
    let selectedPreviewIndex = -1;
    
    // 初始化事件监听
    initEvents();
    
    function initEvents() {
        // 上传区域点击事件
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // 文件选择改变
        fileInput.addEventListener('change', handleFileSelect);
        
        // 拖放事件
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
        
        // 质量滑块更新
        qualitySlider.addEventListener('input', () => {
            qualityValue.textContent = `${qualitySlider.value}%`;
        });
        
        // 缩放选项显示/隐藏
        resizeCheckbox.addEventListener('change', () => {
            resizeOptions.style.display = resizeCheckbox.checked ? 'block' : 'none';
        });
        
        // 宽高比锁定
        widthInput.addEventListener('input', () => {
            if (aspectRatioCheckbox.checked && originalFiles.length > 0 && selectedPreviewIndex >= 0) {
                const file = originalFiles[selectedPreviewIndex];
                if (file.dimensions) {
                    const ratio = file.dimensions.height / file.dimensions.width;
                    heightInput.value = Math.round(widthInput.value * ratio);
                }
            }
        });
        
        heightInput.addEventListener('input', () => {
            if (aspectRatioCheckbox.checked && originalFiles.length > 0 && selectedPreviewIndex >= 0) {
                const file = originalFiles[selectedPreviewIndex];
                if (file.dimensions) {
                    const ratio = file.dimensions.width / file.dimensions.height;
                    widthInput.value = Math.round(heightInput.value * ratio);
                }
            }
        });
        
        // 压缩按钮
        compressBtn.addEventListener('click', compressImages);
        
        // 重置按钮
        resetBtn.addEventListener('click', resetTool);
        
        // 批量下载按钮
        downloadAllBtn.addEventListener('click', downloadAllImages);
        
        // 比较滑块
        comparisonSlider.addEventListener('mousedown', handleSliderDrag);
        comparisonSlider.addEventListener('touchstart', handleSliderDrag, { passive: false });
    }
    
    // 文件选择处理
    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            processFiles(files);
        }
    }
    
    // 拖放处理
    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('drag-over');
    }
    
    function handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('drag-over');
    }
    
    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            processFiles(files);
        }
    }
    
    // 处理上传的文件
    function processFiles(files) {
        // 清空之前的文件
        originalFiles = [];
        processedFiles = [];
        previewContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        comparisonView.style.display = 'none';
        
        // 过滤出图片文件
        const imageFiles = Array.from(files).filter(file => 
            file.type.match(/^image\/(jpeg|png|gif|webp)$/) && file.size <= 20 * 1024 * 1024
        );
        
        if (imageFiles.length === 0) {
            alert('请选择有效的图片文件（JPG, PNG, WEBP, GIF），最大20MB。');
            return;
        }
        
        // 显示压缩界面
        uploadArea.style.display = 'none';
        compressionInterface.style.display = 'block';
        
        // 处理每个文件
        imageFiles.forEach((file, index) => {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    const dimensions = {
                        width: img.width,
                        height: img.height
                    };
                    
                    originalFiles.push({
                        file: file,
                        dataUrl: e.target.result,
                        dimensions: dimensions,
                        name: file.name,
                        type: file.type,
                        size: file.size
                    });
                    
                    // 创建预览卡片
                    const card = createPreviewCard(originalFiles.length - 1, e.target.result, file.name, formatFileSize(file.size));
                    previewContainer.appendChild(card);
                    
                    // 选择第一个图片作为默认预览
                    if (index === 0) {
                        selectPreview(0);
                    }
                };
                img.src = e.target.result;
            };
            
            reader.readAsDataURL(file);
        });
    }
    
    // 创建预览卡片
    function createPreviewCard(index, dataUrl, name, size) {
        const card = document.createElement('div');
        card.className = 'preview-card';
        card.dataset.index = index;
        
        card.innerHTML = `
            <div class="preview-img-container">
                <img src="${dataUrl}" alt="${name}" class="preview-img">
            </div>
            <div class="preview-info">
                <div class="preview-filename">${truncateFilename(name)}</div>
                <div class="preview-filesize">${size}</div>
            </div>
        `;
        
        card.addEventListener('click', () => selectPreview(index));
        
        return card;
    }
    
    // 选择预览图片
    function selectPreview(index) {
        // 移除之前选中的样式
        const cards = previewContainer.querySelectorAll('.preview-card');
        cards.forEach(card => card.classList.remove('selected'));
        
        // 添加新选中的样式
        const selectedCard = previewContainer.querySelector(`.preview-card[data-index="${index}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
        
        selectedPreviewIndex = index;
        
        // 更新尺寸输入框
        const file = originalFiles[index];
        if (file && file.dimensions) {
            widthInput.value = file.dimensions.width;
            heightInput.value = file.dimensions.height;
        }
        
        // 如果有压缩后的图片，显示对比视图
        if (processedFiles[index]) {
            updateComparisonView(index);
        } else {
            comparisonView.style.display = 'none';
        }
    }
    
    // 压缩图片
    async function compressImages() {
        if (originalFiles.length === 0) return;
        
        // 显示进度条
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        
        // 禁用按钮
        compressBtn.disabled = true;
        resetBtn.disabled = true;
        
        // 获取压缩选项
        const quality = parseInt(qualitySlider.value) / 100;
        const format = formatSelect.value;
        const shouldResize = resizeCheckbox.checked;
        const targetWidth = shouldResize ? parseInt(widthInput.value) : null;
        const targetHeight = shouldResize ? parseInt(heightInput.value) : null;
        
        // 清空之前的结果
        processedFiles = [];
        resultsList.innerHTML = '';
        
        try {
            for (let i = 0; i < originalFiles.length; i++) {
                const progress = Math.round((i / originalFiles.length) * 100);
                progressBar.style.width = `${progress}%`;
                
                const original = originalFiles[i];
                const result = await compressImage(original, {
                    quality: quality,
                    format: format,
                    width: targetWidth,
                    height: targetHeight,
                    maintainRatio: aspectRatioCheckbox.checked
                });
                
                processedFiles[i] = result;
                
                // 创建结果项
                const savingsPercent = Math.round((1 - (result.size / original.size)) * 100);
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                resultItem.innerHTML = `
                    <div class="result-preview">
                        <img src="${result.dataUrl}" alt="${result.name}" class="result-img">
                    </div>
                    <div class="result-info">
                        <div class="result-filename">${truncateFilename(result.name)}</div>
                        <div class="result-details">
                            <span>原始: ${formatFileSize(original.size)}</span>
                            <span>压缩后: ${formatFileSize(result.size)}</span>
                            <span class="savings">节省: ${savingsPercent}%</span>
                        </div>
                    </div>
                    <div class="result-actions">
                        <button class="btn btn-sm download-btn" data-index="${i}">
                            <i class="bi bi-download"></i>
                        </button>
                    </div>
                `;
                
                const downloadBtn = resultItem.querySelector('.download-btn');
                downloadBtn.addEventListener('click', () => downloadImage(i));
                
                resultsList.appendChild(resultItem);
            }
            
            // 完成进度
            progressBar.style.width = '100%';
            
            // 显示结果和比较视图
            resultsContainer.style.display = 'block';
            
            // 更新当前选中预览的比较视图
            if (selectedPreviewIndex >= 0) {
                updateComparisonView(selectedPreviewIndex);
            }
        } catch (error) {
            console.error('压缩过程中出错:', error);
            alert('压缩过程中出错: ' + error.message);
        } finally {
            // 启用按钮
            compressBtn.disabled = false;
            resetBtn.disabled = false;
            
            // 3秒后隐藏进度条
            setTimeout(() => {
                progressContainer.style.display = 'none';
            }, 3000);
        }
    }
    
    // 压缩单个图片
    async function compressImage(original, options) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            
            img.onload = function() {
                try {
                    // 创建画布
                    const canvas = document.createElement('canvas');
                    let width = img.width;
                    let height = img.height;
                    
                    // 如果需要调整尺寸
                    if (options.width && options.height) {
                        width = options.width;
                        height = options.height;
                    } else if (options.width) {
                        // 只调整宽度，保持宽高比
                        const ratio = options.width / img.width;
                        width = options.width;
                        height = Math.round(img.height * ratio);
                    } else if (options.height) {
                        // 只调整高度，保持宽高比
                        const ratio = options.height / img.height;
                        height = options.height;
                        width = Math.round(img.width * ratio);
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    // 绘制图片
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    // 确定输出格式
                    let outputType = original.type;
                    let outputExt = getFileExtension(original.name);
                    let filename = original.name;
                    
                    if (options.format !== 'same') {
                        switch (options.format) {
                            case 'jpeg':
                                outputType = 'image/jpeg';
                                outputExt = '.jpg';
                                break;
                            case 'png':
                                outputType = 'image/png';
                                outputExt = '.png';
                                break;
                            case 'webp':
                                outputType = 'image/webp';
                                outputExt = '.webp';
                                break;
                        }
                        
                        // 更新文件名的扩展名
                        filename = changeFileExtension(original.name, outputExt);
                    }
                    
                    // 获取压缩后的数据URL
                    const dataUrl = canvas.toDataURL(outputType, options.quality);
                    
                    // 计算压缩后的大小
                    const size = Math.round(dataUrl.length * 0.75);
                    
                    resolve({
                        name: filename,
                        type: outputType,
                        dataUrl: dataUrl,
                        size: size,
                        dimensions: {
                            width: width,
                            height: height
                        }
                    });
                } catch (err) {
                    reject(err);
                }
            };
            
            img.onerror = function() {
                reject(new Error('图片加载失败'));
            };
            
            img.src = original.dataUrl;
        });
    }
    
    // 更新比较视图
    function updateComparisonView(index) {
        if (!processedFiles[index]) {
            comparisonView.style.display = 'none';
            return;
        }
        
        comparisonView.style.display = 'block';
        
        const original = originalFiles[index];
        const processed = processedFiles[index];
        
        comparisonImage.onload = function() {
            comparisonOriginal.style.backgroundImage = `url(${original.dataUrl})`;
            comparisonCompressed.style.backgroundImage = `url(${processed.dataUrl})`;
            
            // 设置初始比较位置为中间
            comparisonSlider.style.left = '50%';
            comparisonCompressed.style.width = '50%';
            
            comparisonContainer.style.display = 'block';
        };
        
        comparisonImage.src = original.dataUrl;
    }
    
    // 处理比较滑块拖动
    function handleSliderDrag(e) {
        e.preventDefault();
        
        const container = comparisonContainer;
        const containerWidth = container.offsetWidth;
        
        function moveSlider(clientX) {
            const containerRect = container.getBoundingClientRect();
            const position = clientX - containerRect.left;
            const percentage = Math.max(0, Math.min(1, position / containerWidth)) * 100;
            
            comparisonSlider.style.left = `${percentage}%`;
            comparisonCompressed.style.width = `${percentage}%`;
        }
        
        function onMove(moveEvent) {
            const clientX = moveEvent.type === 'touchmove' 
                ? moveEvent.touches[0].clientX 
                : moveEvent.clientX;
            moveSlider(clientX);
        }
        
        function onEnd() {
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup', onEnd);
            document.removeEventListener('touchmove', onMove);
            document.removeEventListener('touchend', onEnd);
        }
        
        // 初始移动
        const clientX = e.type === 'touchstart' 
            ? e.touches[0].clientX 
            : e.clientX;
        moveSlider(clientX);
        
        // 添加移动和结束事件
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onEnd);
        document.addEventListener('touchmove', onMove, { passive: false });
        document.addEventListener('touchend', onEnd);
    }
    
    // 下载单个图片
    function downloadImage(index) {
        if (!processedFiles[index]) return;
        
        const file = processedFiles[index];
        const link = document.createElement('a');
        link.href = file.dataUrl;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    // 批量下载所有图片
    async function downloadAllImages() {
        if (processedFiles.length === 0) return;
        
        // 如果只有一个文件，直接下载
        if (processedFiles.length === 1) {
            downloadImage(0);
            return;
        }
        
        // 显示进度条
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        downloadAllBtn.disabled = true;
        
        try {
            const zip = new JSZip();
            
            // 添加所有文件到zip
            for (let i = 0; i < processedFiles.length; i++) {
                const progress = Math.round((i / processedFiles.length) * 50);
                progressBar.style.width = `${progress}%`;
                
                const file = processedFiles[i];
                const data = dataURLtoBlob(file.dataUrl);
                zip.file(file.name, data);
            }
            
            // 生成zip文件
            progressBar.style.width = '75%';
            const content = await zip.generateAsync({ type: 'blob' });
            
            // 下载zip文件
            progressBar.style.width = '100%';
            saveAs(content, 'compressed-images.zip');
        } catch (error) {
            console.error('批量下载错误:', error);
            alert('批量下载过程中出错: ' + error.message);
        } finally {
            downloadAllBtn.disabled = false;
            
            // 3秒后隐藏进度条
            setTimeout(() => {
                progressContainer.style.display = 'none';
            }, 3000);
        }
    }
    
    // 重置工具
    function resetTool() {
        // 清空文件输入
        fileInput.value = '';
        
        // 重置UI
        uploadArea.style.display = 'block';
        compressionInterface.style.display = 'none';
        comparisonView.style.display = 'none';
        
        // 清空预览
        previewContainer.innerHTML = '';
        resultsList.innerHTML = '';
        
        // 重置存储
        originalFiles = [];
        processedFiles = [];
        selectedPreviewIndex = -1;
        
        // 重置选项
        qualitySlider.value = 80;
        qualityValue.textContent = '80%';
        formatSelect.value = 'same';
        resizeCheckbox.checked = false;
        resizeOptions.style.display = 'none';
    }
    
    // 辅助函数
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function truncateFilename(filename, maxLength = 20) {
        if (filename.length <= maxLength) return filename;
        
        const extension = getFileExtension(filename);
        const name = filename.substring(0, filename.length - extension.length);
        
        if (name.length <= maxLength - 3 - extension.length) {
            return name + extension;
        }
        
        return name.substring(0, maxLength - 3 - extension.length) + '...' + extension;
    }
    
    function getFileExtension(filename) {
        return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 1);
    }
    
    function changeFileExtension(filename, newExt) {
        const lastDotIndex = filename.lastIndexOf('.');
        if (lastDotIndex === -1) return filename + newExt;
        
        return filename.substring(0, lastDotIndex) + newExt;
    }
    
    // 将DataURL转换为Blob
    function dataURLtoBlob(dataURL) {
        const parts = dataURL.split(';base64,');
        const contentType = parts[0].split(':')[1];
        const raw = window.atob(parts[1]);
        const rawLength = raw.length;
        const uInt8Array = new Uint8Array(rawLength);
        
        for (let i = 0; i < rawLength; ++i) {
            uInt8Array[i] = raw.charCodeAt(i);
        }
        
        return new Blob([uInt8Array], { type: contentType });
    }
}); 