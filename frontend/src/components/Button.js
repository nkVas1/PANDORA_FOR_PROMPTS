/**
 * Button Component - Reusable button with variants
 */

export function createButton(options = {}) {
  const button = document.createElement('button');
  button.className = `btn btn--${options.variant || 'primary'} ${options.className || ''}`;
  
  if (options.size) {
    button.classList.add(`btn--${options.size}`);
  }
  
  if (options.icon) {
    const icon = document.createElement('span');
    icon.innerHTML = options.icon;
    button.appendChild(icon);
  }
  
  if (options.label) {
    const label = document.createElement('span');
    label.textContent = options.label;
    button.appendChild(label);
  }
  
  if (options.onClick) {
    button.addEventListener('click', options.onClick);
  }
  
  if (options.disabled) {
    button.disabled = true;
  }
  
  return button;
}

/**
 * Button Group - Group of buttons
 */
export function createButtonGroup(buttons = []) {
  const group = document.createElement('div');
  group.className = 'button-group';
  
  buttons.forEach(btn => {
    group.appendChild(btn);
  });
  
  return group;
}
