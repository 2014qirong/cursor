/**
 * utils.js - 通用工具函数库
 * 包含各种工具页面共用的工具函数
 */

// 文件处理相关工具函数

/**
 * 格式化文件大小
 * @param {number} bytes - 文件大小（字节）
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化后的文件大小字符串
 */
function formatFileSize(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * 获取文件扩展名
 * @param {string} filename - 文件名
 * @returns {string} 文件扩展名（小写）
 */
function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();
}

/**
 * 验证文件类型
 * @param {File} file - 文件对象
 * @param {string[]} allowedTypes - 允许的MIME类型数组
 * @returns {boolean} 是否为允许的文件类型
 */
function validateFileType(file, allowedTypes) {
    return allowedTypes.includes(file.type);
}

/**
 * 验证文件大小
 * @param {File} file - 文件对象
 * @param {number} maxSize - 最大文件大小（字节）
 * @returns {boolean} 是否小于最大允许大小
 */
function validateFileSize(file, maxSize) {
    return file.size <= maxSize;
}

// 图片处理相关工具函数

/**
 * 加载图片
 * @param {string} src - 图片URL或DataURL
 * @returns {Promise<HTMLImageElement>} 加载完成的图片元素
 */
function loadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
    });
}

/**
 * 压缩图片
 * @param {HTMLImageElement|String} source - 图片元素或URL
 * @param {Object} options - 压缩选项
 * @param {number} options.quality - 图片质量（0-1）
 * @param {string} options.type - 图片类型（默认为'image/jpeg'）
 * @param {number} options.maxWidth - 最大宽度（可选）
 * @param {number} options.maxHeight - 最大高度（可选）
 * @returns {Promise<string>} 压缩后的图片DataURL
 */
async function compressImage(source, options = {}) {
    const defaults = {
        quality: 0.8,
        type: 'image/jpeg',
        maxWidth: Infinity,
        maxHeight: Infinity
    };
    
    const settings = { ...defaults, ...options };
    
    let img;
    if (typeof source === 'string') {
        img = await loadImage(source);
    } else {
        img = source;
    }
    
    // 计算新尺寸，保持比例
    let width = img.width;
    let height = img.height;
    
    if (width > settings.maxWidth || height > settings.maxHeight) {
        const ratio = Math.min(
            settings.maxWidth / width,
            settings.maxHeight / height
        );
        width = width * ratio;
        height = height * ratio;
    }
    
    // 创建canvas并绘制图片
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, width, height);
    
    // 输出为DataURL
    return canvas.toDataURL(settings.type, settings.quality);
}

/**
 * 为图片添加水印
 * @param {HTMLImageElement|String} source - 图片元素或URL
 * @param {Object} options - 水印选项
 * @param {string} options.text - 水印文字（如果是文字水印）
 * @param {HTMLImageElement|String} options.image - 水印图片（如果是图片水印）
 * @param {string} options.position - 水印位置（'center', 'topLeft', 'topRight', 'bottomLeft', 'bottomRight'）
 * @param {number} options.opacity - 水印透明度（0-1）
 * @returns {Promise<string>} 添加水印后的图片DataURL
 */
async function addWatermark(source, options = {}) {
    const defaults = {
        text: '',
        image: null,
        position: 'bottomRight',
        opacity: 0.5,
        margin: 10,
        fontSize: 20,
        fontFamily: 'Arial',
        fontColor: 'white',
        fontWeight: 'bold'
    };
    
    const settings = { ...defaults, ...options };
    
    let img;
    if (typeof source === 'string') {
        img = await loadImage(source);
    } else {
        img = source;
    }
    
    // 创建canvas并绘制原图
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    
    // 设置透明度
    ctx.globalAlpha = settings.opacity;
    
    // 绘制水印
    if (settings.text) {
        // 文字水印
        ctx.font = `${settings.fontWeight} ${settings.fontSize}px ${settings.fontFamily}`;
        ctx.fillStyle = settings.fontColor;
        
        const textWidth = ctx.measureText(settings.text).width;
        const textHeight = settings.fontSize;
        
        let x, y;
        
        // 根据位置计算坐标
        switch (settings.position) {
            case 'center':
                x = (canvas.width - textWidth) / 2;
                y = (canvas.height + textHeight) / 2;
                break;
            case 'topLeft':
                x = settings.margin;
                y = settings.margin + textHeight;
                break;
            case 'topRight':
                x = canvas.width - textWidth - settings.margin;
                y = settings.margin + textHeight;
                break;
            case 'bottomLeft':
                x = settings.margin;
                y = canvas.height - settings.margin;
                break;
            case 'bottomRight':
            default:
                x = canvas.width - textWidth - settings.margin;
                y = canvas.height - settings.margin;
                break;
        }
        
        ctx.fillText(settings.text, x, y);
    } else if (settings.image) {
        // 图片水印
        let watermarkImg;
        if (typeof settings.image === 'string') {
            watermarkImg = await loadImage(settings.image);
        } else {
            watermarkImg = settings.image;
        }
        
        let x, y;
        
        // 根据位置计算坐标
        switch (settings.position) {
            case 'center':
                x = (canvas.width - watermarkImg.width) / 2;
                y = (canvas.height - watermarkImg.height) / 2;
                break;
            case 'topLeft':
                x = settings.margin;
                y = settings.margin;
                break;
            case 'topRight':
                x = canvas.width - watermarkImg.width - settings.margin;
                y = settings.margin;
                break;
            case 'bottomLeft':
                x = settings.margin;
                y = canvas.height - watermarkImg.height - settings.margin;
                break;
            case 'bottomRight':
            default:
                x = canvas.width - watermarkImg.width - settings.margin;
                y = canvas.height - watermarkImg.height - settings.margin;
                break;
        }
        
        ctx.drawImage(watermarkImg, x, y);
    }
    
    // 恢复透明度
    ctx.globalAlpha = 1.0;
    
    return canvas.toDataURL('image/png');
}

/**
 * 裁剪图片
 * @param {HTMLImageElement|String} source - 图片元素或URL
 * @param {Object} cropArea - 裁剪区域
 * @param {number} cropArea.x - 起始X坐标
 * @param {number} cropArea.y - 起始Y坐标
 * @param {number} cropArea.width - 裁剪宽度
 * @param {number} cropArea.height - 裁剪高度
 * @returns {Promise<string>} 裁剪后的图片DataURL
 */
async function cropImage(source, cropArea) {
    let img;
    if (typeof source === 'string') {
        img = await loadImage(source);
    } else {
        img = source;
    }
    
    // 创建canvas并绘制裁剪区域
    const canvas = document.createElement('canvas');
    canvas.width = cropArea.width;
    canvas.height = cropArea.height;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(
        img,
        cropArea.x, cropArea.y, cropArea.width, cropArea.height,
        0, 0, cropArea.width, cropArea.height
    );
    
    return canvas.toDataURL('image/png');
}

/**
 * 计算图像指纹（用于图像去重）
 * @param {HTMLImageElement|String} source - 图片元素或URL
 * @returns {Promise<string>} 图片的指纹哈希值
 */
async function calculateImageFingerprint(source) {
    let img;
    if (typeof source === 'string') {
        img = await loadImage(source);
    } else {
        img = source;
    }
    
    // 缩小图片到8x8
    const canvas = document.createElement('canvas');
    canvas.width = 8;
    canvas.height = 8;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, 8, 8);
    
    // 获取像素数据
    const imageData = ctx.getImageData(0, 0, 8, 8).data;
    
    // 计算灰度值
    const grayValues = [];
    for (let i = 0; i < imageData.length; i += 4) {
        const r = imageData[i];
        const g = imageData[i + 1];
        const b = imageData[i + 2];
        
        // 转为灰度 (亮度加权平均法)
        const gray = 0.299 * r + 0.587 * g + 0.114 * b;
        grayValues.push(gray);
    }
    
    // 计算平均值
    const avg = grayValues.reduce((sum, val) => sum + val, 0) / grayValues.length;
    
    // 生成指纹哈希
    let fingerprint = '';
    grayValues.forEach(val => {
        fingerprint += val >= avg ? '1' : '0';
    });
    
    return fingerprint;
}

/**
 * 比较两个图像指纹的相似度
 * @param {string} fingerprint1 - 第一个图像指纹
 * @param {string} fingerprint2 - 第二个图像指纹
 * @returns {number} 相似度百分比（0-100）
 */
function compareFingerprints(fingerprint1, fingerprint2) {
    if (fingerprint1.length !== fingerprint2.length) {
        return 0;
    }
    
    let matchCount = 0;
    for (let i = 0; i < fingerprint1.length; i++) {
        if (fingerprint1[i] === fingerprint2[i]) {
            matchCount++;
        }
    }
    
    return (matchCount / fingerprint1.length) * 100;
}

// 导出所有工具函数
window.utils = {
    formatFileSize,
    getFileExtension,
    validateFileType,
    validateFileSize,
    loadImage,
    compressImage,
    addWatermark,
    cropImage,
    calculateImageFingerprint,
    compareFingerprints
}; 