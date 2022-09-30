const domContainer = document.querySelector('.index');
const root = ReactDOM.createRoot(domContainer);
root.render(e('button',
  { onClick: () => this.setState({ liked: true }) },
  'Нравится'));
