document.addEventListener('DOMContentLoaded', function() {
  // Lấy tất cả các nút có class "close_slide"
  var closeButtons = document.querySelectorAll('.close_slide');

  // Kiểm tra nếu có nút nào được tìm thấy
  if (closeButtons && closeButtons.length > 0) {
      // Lặp qua tất cả các nút và thêm sự kiện click
      closeButtons.forEach(function(button) {
          button.addEventListener('click', function(event) {
              event.preventDefault(); // Ngăn chặn hành động mặc định của thẻ <a>

              // Lấy tất cả các phần tử với class "hidden"
              var hiddenElements = document.querySelectorAll('.hidden');

              // Kiểm tra nếu có phần tử nào được tìm thấy
              if (hiddenElements && hiddenElements.length > 0) {
                  // Lặp qua tất cả các phần tử và ẩn chúng
                  hiddenElements.forEach(function(hiddenElement) {
                      hiddenElement.style.display = 'none'; // Hoặc thêm class để ẩn
                  });
              } else {
                  console.error('Không tìm thấy phần tử nào với class "hidden"!');
              }
          });
      });
  } else {
      console.error('Không tìm thấy nút nào với class "close_slide"!');
  }
});

// click to close slide
document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả các nút có class "close_slide"
    var closeButtons = document.querySelectorAll('.close_slide');
  
    // Kiểm tra nếu có nút nào được tìm thấy
    if (closeButtons && closeButtons.length > 0) {
        // Lặp qua tất cả các nút và thêm sự kiện click
        closeButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault(); // Ngăn chặn hành động mặc định của thẻ <a>
  
                // Lấy tất cả các phần tử với class "hidden" trong thẻ <nav>
                var hiddenElements = document.querySelectorAll('nav .hidden');
  
                // Kiểm tra nếu có phần tử nào được tìm thấy
                if (hiddenElements && hiddenElements.length > 0) {
                    // Lặp qua tất cả các phần tử và kiểm tra trạng thái hiển thị
                    hiddenElements.forEach(function(hiddenElement) {
                        if (hiddenElement.style.display === 'none' || hiddenElement.style.display === '') {
                            hiddenElement.style.display = 'block'; // Hiển thị phần tử
                        } else {
                            hiddenElement.style.display = 'none'; // Ẩn phần tử
                        }
                    });
                } else {
                    console.error('Không tìm thấy phần tử nào với class "hidden" trong thẻ <nav>!');
                }
            });
        });
    } else {
        console.error('Không tìm thấy nút nào với class "close_slide"!');
    }
  });
  
