/**
 * 图片压缩工具 JavaScript
 * 实现图片上传、压缩、预览和下载功能
 */

// 全局变量
const maxFileSize = 10 * 1024 * 1024; // 10MB
let originalImages = []; // 存储原始图片数据
let compressedImages = []; // 存储压缩后的图片数据
let currentImageIndex = 0; // 当前预览的图片索引
let compressInProgress = false;

// 当DOM完全加载后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有事件和功能
    initEvents();
});

// 初始化所有事件监听
function initEvents() {
    // 获取DOM元素
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const qualitySlider = document.getElementById('quality-slider');
    const qualityValue = document.getElementById('quality-value');
    const outputFormat = document.getElementById('output-format');
    const resizeCheckbox = document.getElementById('resize-checkbox');
    const resizeOptions = document.getElementById('resize-options');
    const widthInput = document.getElementById('width-input');
    const heightInput = document.getElementById('height-input');
    const aspectRatioCheckbox = document.getElementById('aspect-ratio-checkbox');
    const renameCheckbox = document.getElementById('rename-checkbox');
    const renameOptions = document.getElementById('rename-options');
    const renamePattern = document.getElementById('rename-pattern');
    const compressBtn = document.getElementById('compress-btn');
    const clearAllBtn = document.getElementById('clear-all-btn');
    const downloadAllBtn = document.getElementById('download-all-btn');
    const copyResultsBtn = document.getElementById('copy-results-btn');
    const batchResults = document.getElementById('batch-results');
    const resultsList = document.getElementById('results-list');
    const imagesCount = document.getElementById('images-count');
    const originalPreview = document.getElementById('original-preview');
    const compressedPreview = document.getElementById('compressed-preview');
    const originalInfo = document.getElementById('original-info');
    const compressedInfo = document.getElementById('compressed-info');
    const statusMessage = document.getElementById('status-message');

    // 拖放事件
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefault, false);
    });

    function preventDefault(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // 拖放区域高亮
    dropArea.addEventListener('dragenter', function() {
        this.classList.add('dragover');
    });
    
    dropArea.addEventListener('dragover', function() {
        this.classList.add('dragover');
    });
    
    dropArea.addEventListener('dragleave', function() {
        this.classList.remove('dragover');
    });
    
    dropArea.addEventListener('drop', handleDrop);

    // 点击上传区域触发文件选择
    dropArea.addEventListener('click', function() {
        fileInput.click();
    });

    // 文件选择变化事件
    fileInput.addEventListener('change', handleFileSelect);

    // 质量滑块事件
    qualitySlider.addEventListener('input', function() {
        qualityValue.textContent = this.value;
    });

    // 调整尺寸复选框事件
    resizeCheckbox.addEventListener('change', function() {
        resizeOptions.classList.toggle('d-none', !this.checked);
    });

    // 重命名复选框事件
    renameCheckbox.addEventListener('change', function() {
        renameOptions.classList.toggle('d-none', !this.checked);
    });

    // 保持宽高比事件
    let originalWidth = 0;
    let originalHeight = 0;
    let aspectRatio = 1;

    widthInput.addEventListener('input', function() {
        if (aspectRatioCheckbox.checked && aspectRatio) {
            heightInput.value = Math.round(parseInt(this.value) / aspectRatio);
        }
    });

    heightInput.addEventListener('input', function() {
        if (aspectRatioCheckbox.checked && aspectRatio) {
            widthInput.value = Math.round(parseInt(this.value) * aspectRatio);
        }
    });

    // 压缩按钮事件
    compressBtn.addEventListener('click', function() {
        if (originalImages.length === 0) {
            showStatusMessage('请先上传图片', 'error');
            return;
        }
        
        compressImages();
    });

    // 清除所有按钮事件
    clearAllBtn.addEventListener('click', function() {
        resetTool();
    });

    // 下载所有按钮事件
    downloadAllBtn.addEventListener('click', function() {
        downloadAllImages();
    });

    // 复制结果按钮事件
    copyResultsBtn.addEventListener('click', function() {
        const resultText = Array.from(resultsList.querySelectorAll('.result-item')).map(item => {
            const name = item.querySelector('.result-name').textContent;
            const stats = item.querySelector('.result-stats').textContent;
            return `${name} - ${stats}`;
        }).join('\n');
        
        navigator.clipboard.writeText(resultText).then(function() {
            showStatusMessage('压缩结果已复制到剪贴板', 'success');
        }).catch(function() {
            showStatusMessage('复制失败，请手动复制', 'error');
        });
    });
}

// 处理文件选择事件
function handleFileSelect(e) {
    if (!e.target.files.length) return;
    
    const files = Array.from(e.target.files);
    processFiles(files);
    
    // 重置文件输入以允许选择同一文件
    e.target.value = '';
}

// 处理拖放事件
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
}

// 处理拖放区域离开
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('drop-area').classList.remove('dragover');
}

// 处理文件拖放
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('drop-area').classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    processFiles(files);
}

// 处理上传的文件
function processFiles(files) {
    // 筛选出图片文件
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    
    // 检查是否有有效图片
    if (imageFiles.length === 0) {
        showStatusMessage('请上传有效的图片文件', 'error');
        return;
    }
    
    // 检查文件大小限制
    const oversizedFiles = imageFiles.filter(file => file.size > maxFileSize);
    if (oversizedFiles.length > 0) {
        showStatusMessage(`${oversizedFiles.length}个文件超过最大限制(10MB)`, 'error');
        return;
    }
    
    // 保存原始图片数据并预览第一张
    originalImages = originalImages.concat(imageFiles);
    document.getElementById('images-count').textContent = originalImages.length;
    
    // 清空压缩图片数据
    compressedImages = [];
    document.getElementById('batch-results').classList.add('d-none');
    document.getElementById('results-list').innerHTML = '';
    
    // 更新预览
    if (originalImages.length > 0) {
        currentImageIndex = 0;
        updatePreview(currentImageIndex);
    }
    
    showStatusMessage(`已添加${imageFiles.length}张图片，共${originalImages.length}张`, 'success');
}

// 为每个图片创建预览卡片
function createPreviewCard(index, dataUrl, name, size) {
    const card = document.createElement('div');
    card.className = 'preview-card';
    card.dataset.index = index;
    
    card.innerHTML = `
        <div class="image-thumbnail">
            <img src="${dataUrl}" alt="${name}">
        </div>
        <div class="image-info">
            <div class="image-name">${truncateFilename(name)}</div>
            <div class="image-size">${formatFileSize(size)}</div>
        </div>
    `;
    
    card.addEventListener('click', function() {
        document.querySelectorAll('.preview-card').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        updatePreview(parseInt(this.dataset.index));
    });
    
    return card;
}

// 选择预览图片
function updatePreview(index) {
    if (index < 0 || index >= originalImages.length) return;
    
    const file = originalImages[index];
    currentImageIndex = index;
    
    // 读取并显示原始图片
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            // 显示图片
            const originalPreview = document.getElementById('original-preview');
            originalPreview.innerHTML = '';
            originalPreview.appendChild(img);
            
            // 更新宽高比
            const aspectRatio = img.naturalWidth / img.naturalHeight;
            
            // 更新尺寸输入框
            document.getElementById('width-input').value = img.naturalWidth;
            document.getElementById('height-input').value = img.naturalHeight;
            
            // 更新信息
            document.getElementById('original-info').innerHTML = `
                <div>${file.name}</div>
                <div>${img.naturalWidth} x ${img.naturalHeight} | ${formatFileSize(file.size)}</div>
            `;
            
            // 清空压缩预览
            document.getElementById('compressed-preview').innerHTML = '<div class="text-center text-muted">尚未压缩</div>';
            document.getElementById('compressed-info').innerHTML = '';
        };
        
        img.className = 'preview-img';
        img.src = e.target.result;
    };
    
    reader.readAsDataURL(file);
}

// 压缩图片
async function compressImages() {
    if (compressInProgress || originalImages.length === 0) return;
    
    compressInProgress = true;
    const resultsList = document.getElementById('results-list');
    resultsList.innerHTML = '';
    
    // 获取压缩选项
    const options = {
        quality: parseInt(document.getElementById('quality-slider').value) / 100,
        format: document.getElementById('output-format').value,
        resize: document.getElementById('resize-checkbox').checked,
        width: parseInt(document.getElementById('width-input').value) || null,
        height: parseInt(document.getElementById('height-input').value) || null,
        keepAspectRatio: document.getElementById('aspect-ratio-checkbox').checked,
        rename: document.getElementById('rename-checkbox').checked,
        renamePattern: document.getElementById('rename-pattern').value
    };
    
    showStatusMessage('开始压缩...', 'info');
    
    // 进度条
    const totalFiles = originalImages.length;
    let processedFiles = 0;
    
    // 批量处理所有图片
    compressedImages = [];
    
    for (let i = 0; i < originalImages.length; i++) {
        try {
            const original = originalImages[i];
            const compressed = await compressImage(original, options, i);
            compressedImages.push(compressed);
            
            // 添加到结果列表
            const li = document.createElement('div');
            li.className = 'result-item';
            
            const originalSize = original.size;
            const compressedSize = compressed.blob.size;
            const savingsPercent = ((1 - (compressedSize / originalSize)) * 100).toFixed(2);
            const savingsClass = savingsPercent > 50 ? 'text-success' : 
                               savingsPercent > 20 ? 'text-warning' : 'text-danger';
            
            li.innerHTML = `
                <div class="result-thumbnail">
                    <img src="${compressed.dataUrl}" alt="${compressed.fileName}">
                </div>
                <div class="result-info">
                    <div class="result-name">${compressed.fileName}</div>
                    <div class="result-stats">
                        <span>${formatFileSize(originalSize)} → ${formatFileSize(compressedSize)}</span>
                        <span class="${savingsClass}">节省: ${savingsPercent}%</span>
                    </div>
                </div>
                <div class="result-actions">
                    <button class="action-btn download-btn" title="下载图片">
                        <i class="bi bi-download"></i>
                    </button>
                </div>
            `;
            
            // 下载单个图片
            const downloadBtn = li.querySelector('.download-btn');
            downloadBtn.addEventListener('click', function() {
                downloadImage(i);
            });
            
            resultsList.appendChild(li);
            
            // 更新进度
            processedFiles++;
            
            // 如果当前索引与预览索引匹配，更新压缩后预览
            if (i === currentImageIndex) {
                updateCompressedPreview(compressed);
            }
        } catch (error) {
            console.error(`压缩图片 ${i} 失败:`, error);
            showStatusMessage(`压缩图片 ${originalImages[i].name} 失败`, 'error');
        }
    }
    
    // 显示批量结果面板
    document.getElementById('batch-results').classList.remove('d-none');
    
    compressInProgress = false;
    showStatusMessage(`成功压缩 ${processedFiles} 张图片`, 'success');
}

// 压缩单个图片
async function compressImage(original, options, index) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const img = new Image();
            
            img.onload = function() {
                // 创建canvas
                const canvas = document.createElement('canvas');
                let width = img.naturalWidth;
                let height = img.naturalHeight;
                
                // 调整尺寸
                if (options.resize && options.width && options.height) {
                    width = options.width;
                    height = options.height;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                // 绘制图片到canvas
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
                // 确定输出格式
                let format = options.format;
                let mimeType;
                let fileExtension;
                
                if (format === 'original') {
                    // 获取原始格式
                    const originalType = original.type;
                    if (originalType.includes('jpeg') || originalType.includes('jpg')) {
                        mimeType = 'image/jpeg';
                        fileExtension = 'jpg';
                    } else if (originalType.includes('png')) {
                        mimeType = 'image/png';
                        fileExtension = 'png';
                    } else if (originalType.includes('webp')) {
                        mimeType = 'image/webp';
                        fileExtension = 'webp';
                    } else if (originalType.includes('gif')) {
                        mimeType = 'image/gif';
                        fileExtension = 'gif';
                    } else {
                        // 默认为JPEG
                        mimeType = 'image/jpeg';
                        fileExtension = 'jpg';
                    }
                } else {
                    // 使用选定的格式
                    switch (format) {
                        case 'jpeg':
                            mimeType = 'image/jpeg';
                            fileExtension = 'jpg';
                            break;
                        case 'png':
                            mimeType = 'image/png';
                            fileExtension = 'png';
                            break;
                        case 'webp':
                            mimeType = 'image/webp';
                            fileExtension = 'webp';
                            break;
                        default:
                            mimeType = 'image/jpeg';
                            fileExtension = 'jpg';
                    }
                }
                
                // 生成压缩后的DataURL
                const compressedDataUrl = canvas.toDataURL(mimeType, options.quality);
                
                // 生成文件名
                let fileName = original.name;
                
                if (options.rename && options.renamePattern) {
                    const nameWithoutExt = fileName.substring(0, fileName.lastIndexOf('.'));
                    fileName = options.renamePattern.replace('{index}', index + 1).replace('{name}', nameWithoutExt);
                    fileName = `${fileName}.${fileExtension}`;
                } else {
                    // 仅更改扩展名
                    fileName = fileName.substring(0, fileName.lastIndexOf('.')) + '.' + fileExtension;
                }
                
                // 转换为Blob
                const blob = dataURLtoBlob(compressedDataUrl);
                
                resolve({
                    fileName: fileName,
                    dataUrl: compressedDataUrl,
                    blob: blob,
                    width: width,
                    height: height,
                    size: blob.size
                });
            };
            
            img.onerror = function() {
                reject(new Error('图片加载失败'));
            };
            
            img.src = e.target.result;
        };
        
        reader.onerror = function() {
            reject(new Error('文件读取失败'));
        };
        
        reader.readAsDataURL(original);
    });
}

// 更新压缩后预览
function updateCompressedPreview(compressed) {
    const compressedPreview = document.getElementById('compressed-preview');
    const compressedInfo = document.getElementById('compressed-info');
    
    compressedPreview.innerHTML = '';
    
    const img = new Image();
    img.src = compressed.dataUrl;
    img.className = 'preview-img';
    compressedPreview.appendChild(img);
    
    compressedInfo.innerHTML = `
        <div>${compressed.fileName}</div>
        <div>${compressed.width} x ${compressed.height} | ${formatFileSize(compressed.size)}</div>
        <div class="mt-2">
            <button class="btn btn-sm btn-primary download-preview-btn">
                <i class="bi bi-download"></i> 下载
            </button>
        </div>
    `;
    
    // 下载按钮
    const downloadBtn = compressedInfo.querySelector('.download-preview-btn');
    downloadBtn.addEventListener('click', function() {
        downloadImage(currentImageIndex);
    });
}

// 下载单个图片
function downloadImage(index) {
    if (index < 0 || index >= compressedImages.length) return;
    
    const compressed = compressedImages[index];
    const url = URL.createObjectURL(compressed.blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = compressed.fileName;
    document.body.appendChild(a);
    a.click();
    
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}

// 下载所有图片为ZIP
async function downloadAllImages() {
    if (compressedImages.length === 0) {
        showStatusMessage('没有可下载的图片', 'error');
        return;
    }
    
    showStatusMessage('正在准备ZIP文件...', 'info');
    
    try {
        const zip = new JSZip();
        
        // 添加所有压缩后的图片到ZIP
        compressedImages.forEach((image, index) => {
            zip.file(image.fileName, image.blob);
        });
        
        // 生成ZIP文件
        const zipContent = await zip.generateAsync({
            type: 'blob',
            compression: 'DEFLATE',
            compressionOptions: {
                level: 9
            }
        });
        
        // 下载ZIP文件
        const url = URL.createObjectURL(zipContent);
        const a = document.createElement('a');
        a.href = url;
        a.download = '压缩图片.zip';
        document.body.appendChild(a);
        a.click();
        
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
        
        showStatusMessage('ZIP文件已生成，开始下载', 'success');
    } catch (error) {
        console.error('生成ZIP文件失败:', error);
        showStatusMessage('生成ZIP文件失败', 'error');
    }
}

// 重置工具状态
function resetTool() {
    // 清空图片数据
    originalImages = [];
    compressedImages = [];
    currentImageIndex = 0;
    
    // 更新UI
    document.getElementById('images-count').textContent = '0';
    document.getElementById('original-preview').innerHTML = '<div class="text-center text-muted">无预览</div>';
    document.getElementById('compressed-preview').innerHTML = '<div class="text-center text-muted">无预览</div>';
    document.getElementById('original-info').innerHTML = '';
    document.getElementById('compressed-info').innerHTML = '';
    document.getElementById('results-list').innerHTML = '';
    document.getElementById('batch-results').classList.add('d-none');
    
    // 重置表单
    document.getElementById('quality-slider').value = 85;
    document.getElementById('quality-value').textContent = '85';
    document.getElementById('output-format').value = 'original';
    document.getElementById('resize-checkbox').checked = false;
    document.getElementById('resize-options').classList.add('d-none');
    document.getElementById('rename-checkbox').checked = false;
    document.getElementById('rename-options').classList.add('d-none');
    document.getElementById('rename-pattern').value = 'compressed_{index}';
    
    showStatusMessage('所有内容已重置', 'info');
}

// 显示状态消息
function showStatusMessage(message, type = 'info') {
    const statusMessage = document.getElementById('status-message');
    statusMessage.textContent = message;
    statusMessage.className = 'status-message';
    
    // 添加类型样式
    switch (type) {
        case 'success':
            statusMessage.classList.add('status-success');
            break;
        case 'error':
            statusMessage.classList.add('status-error');
            break;
        case 'warning':
            statusMessage.classList.add('status-warning');
            break;
        default:
            statusMessage.classList.add('status-info');
    }
    
    statusMessage.style.display = 'block';
    
    // 3秒后自动隐藏
    setTimeout(() => {
        statusMessage.style.display = 'none';
    }, 3000);
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 截断文件名
function truncateFilename(filename, maxLength = 20) {
    if (filename.length <= maxLength) return filename;
    
    const extension = filename.split('.').pop();
    const name = filename.substring(0, filename.lastIndexOf('.'));
    
    if (name.length <= maxLength - 4) return filename;
    
    return name.substring(0, maxLength - 4) + '...' + (extension ? `.${extension}` : '');
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