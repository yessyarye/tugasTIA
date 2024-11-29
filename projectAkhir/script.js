// Menambahkan event listener untuk tombol "Daftar di sini"
document.getElementById("go-to-signup").addEventListener("click", () => {
  document.getElementById("form-container").style.transform =
    "translateX(-50%)";
});

// Menambahkan event listener untuk tombol "Masuk" (atau sejenisnya) jika Anda perlu kembali
document.getElementById("go-to-login").addEventListener("click", () => {
  document.getElementById("form-container").style.transform = "translateX(0)";
});

// document.addEventListener("DOMContentLoaded", function () {
//     let eyeicon = document.getElementById("eyeicon");
//     let password = document.getElementById("password");
  
//     eyeicon.addEventListener("click", () => {
//       if (password.type === "password") {
//         password.type = "text"; // Ubah tipe input menjadi teks
//         eyeicon.src = "assets/eye-open.png"; // Ganti ikon mata menjadi terbuka
//       } else {
//         password.type = "password"; // Ubah tipe input menjadi password
//         eyeicon.src = "assets/eye-close.png"; // Ganti ikon mata menjadi tertutup
//       }
//     });
  
//     // Menangani saat form dikirim
//     document.querySelector("form").addEventListener("submit", function (event) {
//       let role = document.querySelector('input[name="role"]:checked');
      
//       if (!role) {
//         alert("Pilih jenis login (Admin atau User)!");
//         event.preventDefault(); // Mencegah form dikirim jika tidak ada pilihan role
//       } else {
//         console.log("Role yang dipilih: " + role.value);
//         // Proses lanjut untuk login berdasarkan role (Admin atau User)
//       }
//     });
//   });
  