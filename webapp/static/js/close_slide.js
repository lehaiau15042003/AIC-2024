// let clickClose = false
// document.getElementsByClassName('close_slide').addEventListener('click', function(event){
//     event.preventDefaulse();

//     if (clickClose) {
//         this.innerHTML = 'Click to close slide';
//     } else {
//         this.innerHTML = 'The text is longer';
//     }
//     clickClose = !clickClose;
// })

// const clickBox = document.querySelectorAll('.close_slide');
// const btnClick = document.querySelector('#btn_close');
// const showSlide = document.querySelector('.menu_icon');

// const lineContainer = document.querySelector(".close_slide");
// const menu = document.querySelector(".menu_icon");

// lineContainer.addEventListener("click", () => {
//   lineContainer.classList.toggle("active");
//   menu.classList.toggle("open");
// });

// Đảm bảo mã JavaScript chỉ chạy sau khi toàn bộ DOM đã tải xong
// Đảm bảo mã JavaScript chỉ chạy sau khi toàn bộ DOM đã tải xong
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

