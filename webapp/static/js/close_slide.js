document.addEventListener('DOMContentLoaded', function() {
  // Lấy tất cả các nút có class "close_slide"
  var closeButtons = document.querySelectorAll('.close_slide');

  // Kiểm tra nếu có nút nào được tìm thấy
  if (closeButtons && closeButtons.length > 0) {
      // Lặp qua tất cả các nút và thêm sự kiện click
      closeButtons.forEach(function(button) {
          button.addEventListener('click', function(event) {
            //   event.preventDefault(); 
              // Ngăn chặn hành động mặc định của thẻ <a>

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


// click close_clide to swap width
document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả các nút có class "close_slide"
    var closeButtons = document.querySelectorAll('.close_slide');
  
    // Kiểm tra nếu có nút nào được tìm thấy
    if (closeButtons && closeButtons.length > 0) {
        // Lặp qua tất cả các nút và thêm sự kiện click
        closeButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault(); // Ngăn chặn hành động mặc định của thẻ <a>

                // Lấy thẻ <nav>
                var navElement = document.querySelector('nav');
                // Lấy các phần tử với class .menu_icon và .support
                var menuIcon = document.querySelector('.menu_icon');
                var support = document.querySelector('.support');
                var hidden = document.querySelector('nav .hidden');
                var main = document.querySelector('main')

                // Kiểm tra chiều rộng hiện tại của thẻ <nav>
                if (navElement.style.width === '5%') {
                    // Nếu width của nav đang là 5%, đặt lại về giá trị ban đầu
                    navElement.style.width = '20%'; // Giả sử 20% là width ban đầu của nav
                    
                    menuIcon.style.paddingBottom = '20%';
                    menuIcon.style.width = '40%';   // Đặt lại width của .menu_icon (giả sử 50%)
                    support.style.width = '100%';    // Đặt lại width của .support (giả sử 50%)
                    support.style.paddingLeft = '5%';
                    // hidden.style.width = '100%';
                } 
                else {
                    // khi click vào thẻ nav và kiểm chứng được là thẻ nav đang 20% và thực hiện thay đổi trong đây
                    // Nếu không, đặt width của nav thành 5%, và tăng width của .menu_icon và .support
                    navElement.style.width = '5%';
                    menuIcon.style.paddingLeft = '5%';
                    menuIcon.style.paddingLeft = '5%';
                    menuIcon.style.paddingTop = '10%';
                    menuIcon.style.width = '150%';   // Tăng width của .menu_icon
                    support.style.width = '300%';    // Tăng width của .support
                    support.style.paddingLeft = '20%';
                    main.style.width = '150%';
                    // main.style.width = '80%';
                    hidden.style.width = '200%';
                    
                }
            });
        });
    } else {
        console.error('Không tìm thấy nút nào với class "close_slide"!');
    }
});



//   show_inf
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
                    // Lặp qua tất cả các phần tử và kiểm tra trạng thái hiển thị
                    hiddenElements.forEach(function(hiddenElement) {
                        if (hiddenElement.style.display === 'none' || hiddenElement.style.display === '') {
                            hiddenElement.style.display = 'block'; // Hiển thị phần tử
                        } else {
                            hiddenElement.style.display = 'none'; // Ẩn phần tử
                        }
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

