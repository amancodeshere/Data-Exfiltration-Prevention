// Update the data on the page here
function updateData(data) {
    const packetList = document.getElementById('packet-list');
    packetList.innerHTML = '';
    data.forEach(packet => {
        const listItem = document.createElement('li');
        listItem.textContent = packet;
        packetList.appendChild(listItem);
    });
}

// Listen for 'update_data' events
socket.on('update_data', function(data) {
    updateData(data);
});