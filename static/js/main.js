// Toast Notification System
class ToastManager {
  constructor() {
    this.container = this.createContainer()
  }

  createContainer() {
    let container = document.querySelector(".toast-container")
    if (!container) {
      container = document.createElement("div")
      container.className = "toast-container"
      document.body.appendChild(container)
    }
    return container
  }

  show(message, type = "info", duration = 3000) {
    const toast = document.createElement("div")
    toast.className = `toast ${type}`

    const titles = {
      success: "Thành công",
      error: "Lỗi",
      warning: "Cảnh báo",
      info: "Thông tin",
    }

    toast.innerHTML = `
      <div class="toast-header">
        <div class="toast-title">${titles[type]}</div>
        <button class="toast-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
      </div>
      <div class="toast-message">${message}</div>
      <div class="toast-progress"></div>
    `

    this.container.appendChild(toast)

    // Auto remove after duration
    setTimeout(() => {
      if (toast.parentElement) {
        toast.style.animation = "slideOut 0.3s ease-out"
        setTimeout(() => toast.remove(), 300)
      }
    }, duration)

    return toast
  }

  success(message, duration) {
    return this.show(message, "success", duration)
  }

  error(message, duration) {
    return this.show(message, "error", duration)
  }

  warning(message, duration) {
    return this.show(message, "warning", duration)
  }

  info(message, duration) {
    return this.show(message, "info", duration)
  }
}

// Global toast instance
const toast = new ToastManager()

// Thay thế tất cả alert() bằng toast
window.showAlert = (message, type = "info") => {
  toast.show(message, type)
}

// Cart badge management
let cartCount = 0

async function updateCartBadge() {
  try {
    const response = await fetch("/api/cart")
    if (response.ok) {
      const cartItems = await response.json()
      cartCount = cartItems.reduce((total, item) => total + item.quantity, 0)

      const badge = document.querySelector(".cart-badge")
      if (badge) {
        if (cartCount > 0) {
          badge.textContent = `(${cartCount})`
          badge.classList.remove("hidden")
        } else {
          badge.classList.add("hidden")
        }
      }
    }
  } catch (error) {
    console.log("Could not update cart badge")
  }
}

// Các hàm JavaScript chung cho toàn bộ website

// Kiểm tra trạng thái đăng nhập
async function checkLoginStatus() {
  try {
    const response = await fetch("/api/user")
    if (response.ok) {
      const user = await response.json()
      updateNavForLoggedInUser(user)
      updateCartBadge() // Update cart badge when user is logged in
      return user
    }
    return null
  } catch (error) {
    console.log("User not logged in")
    return null
  }
}

// Cập nhật thanh điều hướng cho người dùng đã đăng nhập
function updateNavForLoggedInUser(user) {
  const nav = document.querySelector("nav.nav")
  const loginLink = [...nav.children].find((a) => a.textContent.includes("Đăng nhập"))
  if (loginLink) loginLink.remove()

  // Add cart badge to cart link
  const cartLink = [...nav.children].find((a) => a.textContent.includes("Giỏ hàng"))
  if (cartLink && !cartLink.querySelector(".cart-badge")) {
    cartLink.classList.add("cart-link")
    const badge = document.createElement("span")
    badge.className = "cart-badge hidden"
    badge.textContent = "0"
    cartLink.appendChild(badge)
  }

  const greeting = document.createElement("span")
  greeting.textContent = `Xin chào, ${user.name}`
  greeting.style.marginLeft = "20px"
  greeting.style.fontWeight = "bold"
  nav.appendChild(greeting)

  const logout = document.createElement("a")
  logout.textContent = "Đăng xuất"
  logout.href = "#"
  logout.style.marginLeft = "20px"
  logout.onclick = async () => {
    await fetch("/api/logout", { method: "POST" })
    location.reload()
  }
  nav.appendChild(logout)
}

// Thêm sản phẩm vào giỏ hàng
async function addToCart(productId, quantity = 1) {
  try {
    const response = await fetch("/api/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_id: productId,
        quantity: quantity,
      }),
    })

    const result = await response.json()

    if (response.ok) {
      toast.success("Sản phẩm đã được thêm vào giỏ hàng!")
      updateCartBadge() // Update cart badge after adding item
      return true
    } else {
      if (result.error === "Vui lòng đăng nhập") {
        toast.warning("Bạn cần đăng nhập để thêm sản phẩm.")
        setTimeout(() => {
          window.location.href = "/login"
        }, 1500)
      } else {
        toast.error(result.error)
      }
      return false
    }
  } catch (error) {
    console.error("Error adding to cart:", error)
    toast.error("Có lỗi xảy ra. Vui lòng thử lại.")
    return false
  }
}

// Lấy tham số từ URL
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get(param)
}

// Định dạng giá tiền
function formatPrice(price) {
  return price.toLocaleString("vi-VN") + "₫"
}
