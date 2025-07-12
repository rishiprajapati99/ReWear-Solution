const form = document.getElementById('addItemForm');
const itemsContainer = document.getElementById('itemsContainer');

// Placeholder image in case of broken/invalid URL
const defaultImage = "https://via.placeholder.com/300x200?text=No+Image";

// Load items from localStorage
function loadItems() {
  const items = JSON.parse(localStorage.getItem('myItems')) || [];
  itemsContainer.innerHTML = ''; // Clear

  items.forEach((item, index) => {
    const image = item.image || defaultImage;
    const card = `
      <div class="item-card">
        <img src="${image}" alt="${item.name}" onerror="this.src='${defaultImage}'" />
        <h2>${item.name}</h2>
        <p>${item.size} · ${item.city}</p>
        <button onclick="deleteItem(${index})">🗑️ Delete</button>
      </div>
    `;
    itemsContainer.innerHTML += card;
  });
}

// Save a new item
form.addEventListener('submit', function (e) {
  e.preventDefault();

  const newItem = {
    name: document.getElementById('name').value.trim(),
    size: document.getElementById('size').value.trim(),
    city: document.getElementById('city').value.trim(),
    image: document.getElementById('image').value.trim(),
  };

  if (!newItem.name || !newItem.size || !newItem.city || !newItem.image) {
    alert("Please fill in all fields.");
    return;
  }

  const items = JSON.parse(localStorage.getItem('myItems')) || [];
  items.push(newItem);
  localStorage.setItem('myItems', JSON.stringify(items));
  form.reset();
  loadItems();
});

// Delete an item
function deleteItem(index) {
  const items = JSON.parse(localStorage.getItem('myItems')) || [];
  items.splice(index, 1);
  localStorage.setItem('myItems', JSON.stringify(items));
  loadItems();
}

loadItems();
