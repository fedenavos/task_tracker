document.addEventListener('DOMContentLoaded', (event) => {
  const taskCards = document.querySelectorAll('.task-card');
  taskCards.forEach(card => {
    card.addEventListener('dragstart', handleDragStart);
  });

  // Definir el comportamiento para las columnas de tareas
  const taskColumns = document.querySelectorAll('.task-column');
  taskColumns.forEach(column => {
    column.addEventListener('dragover', handleDragOver);
    column.addEventListener('drop', handleDrop);
  });
});

function handleDragStart(e) {
  e.dataTransfer.setData('text/plain', e.target.id);
}

function handleDragOver(e) {
  if (e.target.classList.contains('task-column')) {
    e.preventDefault();
  }
}

function handleDrop(e) {
  e.preventDefault();
  const taskId = e.dataTransfer.getData('text/plain');
  const card = document.getElementById(taskId);
  let oldState = card.parentNode.id;
  e.target.appendChild(card);

  updateTaskState(taskId, e.target.id, oldState);
}

const form = document.querySelector('.new-task-form');

form.addEventListener('submit', (event) => {
  fetch('/api/tasks/', {
    method: 'POST',
    body: new FormData(form)
  })
    .then(response => response.json())
    .then(data => {
      window.location.reload();
    });
});

document.querySelectorAll('.btn-delete').forEach(button => {
  button.addEventListener('click', function() {
      const taskId = this.getAttribute('data-task-id');
      deleteTask(taskId);
  });
});

const stateMapping = {
  'planned': 'Planned',
  'in-progress': 'In Progress',
  'completed': 'Completed'
};

function moveTaskToNewState(taskId, newState) {
  const taskElement = document.getElementById(`${taskId}`);

  taskElement.parentNode.removeChild(taskElement);

  const newStateList = document.getElementById(newState);
  newStateList.appendChild(taskElement);
}

function updateTaskState(taskId, newState, oldState) {
  url = "/api/tasks/" + taskId + "/";
  fetch(url, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: taskId,
      state: stateMapping[newState]
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      moveTaskToNewState(taskId, newState);
      getNewTotalEstimateAndRender(oldState);
      getNewTotalEstimateAndRender(newState);
    })
    .catch((error) => {
      console.error('Error:', error);
      displayErrorMessage('Something went wrong. Please try again.');
    });
}

function deleteTask(taskId) {
  state = document.getElementById(taskId).parentNode.id;
  url = "/api/tasks/" + taskId + "/";
  fetch(url, {
    method: 'DELETE'
  })
    .then(() => {
      console.log('Success: task deleted');
      const taskElement = document.getElementById(`${taskId}`);
      taskElement.parentNode.removeChild(taskElement);
      getNewTotalEstimateAndRender(state);
    })
    .catch((error) => {
      console.error('Error:', error);
      displayErrorMessage('Something went wrong. Please try again.');
    });
}

function getNewTotalEstimateAndRender(state) {
  url = "/api/tasks/total_estimate?state=" + stateMapping[state];

  fetch(url)
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      const totalEstimateElement = document.querySelector(`#${state} .total-estimate`);
      totalEstimateElement.innerHTML = `Total days: ${data.total_estimate}`;
    })
    .catch((error) => {
      console.error('Error:', error);
      displayErrorMessage('Something went wrong. Please try again.');
    });
}

function displayErrorMessage(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = message;

  document.body.appendChild(errorDiv);

  setTimeout(() => {
      errorDiv.remove();
  }, 5000);
}