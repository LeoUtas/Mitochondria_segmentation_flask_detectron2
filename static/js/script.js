// handle the typing effect
const text = "All models are wrong, but some are useful";
let index = 0;
const outputElement = document.getElementById('typing-text');

function type() {
    if (index < text.length) {
        outputElement.textContent += text.charAt(index);
        index++;
        setTimeout(type, 100);  // typing speed
    } else {
        setTimeout(erase, 1000);  // delay before erasing
    }
}

function erase() {
    if (index > 0) {
        outputElement.textContent = text.substring(0, index - 1);
        index--;
        setTimeout(erase, 100);  // erasing speed
    } else {
        setTimeout(type, 1000);  // delay before retyping
    }
}

document.addEventListener('DOMContentLoaded', function () {
    type();
});


// Handle the loading html compare_images
document.addEventListener('DOMContentLoaded', function () {
    let currentIndex = 1;
    const totalImages = 165;

    const iframe_detectron2 = document.getElementById('image-iframe-detectron2');
    const iframe_YOLOv8 = document.getElementById('image-iframe-YOLOv8');
    const barplotArea_detectron2 = document.getElementById('barplotArea-detectron2');
    const barplotArea_YOLOv8 = document.getElementById('barplotArea-YOLOv8');
    const barplotCount_detectron2 = document.getElementById('barplotCount-detectron2');
    const barplotCount_YOLOv8 = document.getElementById('barplotCount-YOLOv8');
    const prevButton_detectron2 = document.getElementById('prevButton-detectron2');
    const nextButton_detectron2 = document.getElementById('nextButton-detectron2');
    const prevButton_YOLOv8 = document.getElementById('prevButton-YOLOv8');
    const nextButton_YOLOv8 = document.getElementById('nextButton-YOLOv8');
    const imageIndexLabel_detectron2 = document.getElementById('imageIndexLabel-detectron2');
    const imageIndexLabel_YOLOv8 = document.getElementById('imageIndexLabel-YOLOv8');

    function updateIframeSrc(index) {
        const formattedIndex = String(index).padStart(3, '0');
        
        // Set the src for iframe
        const iframe_detectron2_Url = `../static/compare_images_detectron2/test_${formattedIndex}.html`;
        iframe_detectron2.src = iframe_detectron2_Url;

        const iframe_YOLOv8_Url = `../static/compare_images_YOLOv8/test_${formattedIndex}.html`;
        iframe_YOLOv8.src = iframe_YOLOv8_Url;

        // Set the src for bar plot area image
        const barplotArea_detectron2_Url = `../static/compare_barplots_detectron2/barplot_area_${formattedIndex}.png`;
        barplotArea_detectron2.src = barplotArea_detectron2_Url;

        const barplotArea_YOLOv8_Url = `../static/compare_barplots_YOLOv8/barplot_area_${formattedIndex}.png`;
        barplotArea_YOLOv8.src = barplotArea_YOLOv8_Url;

        // Set the src for bar plot area image
        const barplotCount_detectron2_Url = `../static/compare_barplots_detectron2/barplot_count_${formattedIndex}.png`;
        barplotCount_detectron2.src = barplotCount_detectron2_Url;

        const barplotCount_YOLOv8_Url = `../static/compare_barplots_YOLOv8/barplot_count_${formattedIndex}.png`;
        barplotCount_YOLOv8.src = barplotCount_YOLOv8_Url;

        // Update the image index label
        imageIndexLabel_detectron2.textContent = `Image # : ${index}`;
        imageIndexLabel_YOLOv8.textContent = `Image # : ${index}`;
    }

    prevButton_detectron2.addEventListener('click', function() {
        if (currentIndex > 1) {
            currentIndex--;
            updateIframeSrc(currentIndex);
        }
    });

    nextButton_detectron2.addEventListener('click', function() {
        if (currentIndex < totalImages) {
            currentIndex++;
            updateIframeSrc(currentIndex);
        }
    });

    prevButton_YOLOv8.addEventListener('click', function() {
        if (currentIndex > 1) {
            currentIndex--;
            updateIframeSrc(currentIndex);
        }
    });

    nextButton_YOLOv8.addEventListener('click', function() {
        if (currentIndex < totalImages) {
            currentIndex++;
            updateIframeSrc(currentIndex);
        }
    });

    // Initial load
    updateIframeSrc(currentIndex);
});


// to resize iframe (HTML file) and barplot image for better visual
document.addEventListener('DOMContentLoaded', function () {
    const iframe_detectron2 = document.getElementById('image-iframe-detectron2');
    const iframe_YOLOv8 = document.getElementById('image-iframe-YOLOv8');
    const iframeCard = document.getElementById('iframeCard');
    const barplotArea_detectron2 = document.getElementById('barplotArea-detectron2');
    const barplotAreaCard = document.getElementById('barplotAreaCard');
    const barplotCount_detectron2 = document.getElementById('barplotCount-detectron2');
    const barplotCountCard = document.getElementById('barplotCountCard');

    function resizeIframe() {
        const scale_detectron2 = (iframeCard.offsetWidth) / iframe_detectron2.offsetWidth;
        iframe_detectron2.style.transform = `scale(${scale_detectron2})`;
        const scale_YOLOv8 = (iframeCard.offsetWidth) / iframe_YOLOv8.offsetWidth;
        iframe_YOLOv8.style.transform = `scale(${scale_YOLOv8})`;        
    }

    function resizeBarplot(image, card) {
        image.style.width = (card.offsetWidth - 15) + 'px';
        image.style.height = 'auto';
    }

    function resizeItems() {
        resizeIframe();
        resizeBarplot(barplotArea_detectron2, barplotAreaCard);
        resizeBarplot(barplotCount_detectron2, barplotCountCard);
    }

    // Resize on window resize
    window.addEventListener('resize', resizeItems);

    // Initial resize
    resizeItems();
});


// Display the COCOmetrics tables
async function loadMetrics() {
    try {
        const response = await fetch('../static/COCOmetrics/test15_COCOmetrics.json'); // Updated path
        const data = await response.json();
        
        const bboxTable = document.getElementById('bbox-table');
        const segmTable = document.getElementById('segm-table');

        const bboxMetricsRow = bboxTable.createTHead().insertRow();
        const bboxValuesRow = bboxTable.createTBody().insertRow();
        Object.entries(data.bbox).forEach(([key, value]) => {
            const headerCell = document.createElement('th');
            headerCell.innerText = key;
            bboxMetricsRow.appendChild(headerCell);

            const valueCell = document.createElement('td');
            valueCell.innerText = isNaN(value) ? 'N/A' : value.toFixed(2); // Handle NaN values
            bboxValuesRow.appendChild(valueCell);
        });

        const segmMetricsRow = segmTable.createTHead().insertRow();
        const segmValuesRow = segmTable.createTBody().insertRow();
        Object.entries(data.segm).forEach(([key, value]) => {
            const headerCell = document.createElement('th');
            headerCell.innerText = key;
            segmMetricsRow.appendChild(headerCell);

            const valueCell = document.createElement('td');
            valueCell.innerText = isNaN(value) ? 'N/A' : value.toFixed(2); // Handle NaN values
            segmValuesRow.appendChild(valueCell);
        });

    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    loadMetrics();
});

