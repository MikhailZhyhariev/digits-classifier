import React, { Component } from 'react';
import './DrawField.css';

class DrawField extends Component {
  constructor(props) {
    super(props);

    this.startDraw = this.startDraw.bind(this);
    this.handleDraw = this.handleDraw.bind(this);
    this.clearCanvas = this.clearCanvas.bind(this);

    this.state = {
      isDrawing: false
    }
  }

  componentDidMount() {
    const ctx = this.refs.field.getContext('2d');
    ctx.lineWidth = 2;

    window.addEventListener('start', this.startDraw())
  }

  componentWillUnmount() {
    window.removeEventListener('start', this.startDraw())
  }

  startDraw() {
    window.onkeydown = (event) => {
      const ctx = this.refs.field.getContext('2d');
      const { isDrawing } = this.state;

      if (event.keyCode === 32) {
        if (!isDrawing) ctx.beginPath();
        else ctx.closePath();

        this.setState({
          isDrawing: !isDrawing
        })
      }
    }
  }

  clearCanvas() {
    const ctx = this.refs.field.getContext('2d');
    ctx.clearRect(0, 0, 500, 500);
  }

  handleDraw(event) {
    const coord = this.refs.field.getBoundingClientRect();
    const ctx = this.refs.field.getContext('2d');

    const x = event.clientX - coord.left;
    const y = event.clientY - coord.top;

    if (this.state.isDrawing) {
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  }

  render() {
    const { handleDraw, clearCanvas } = this;

    return (
      <div className="draw-field">
        <canvas width="500"
                height="500"
                ref="field"
                onMouseMove={handleDraw} />
        <div className="buttons">
          <button className="button clear"
                  onClick={clearCanvas}>
                  Очистить
          </button>
          <button className="button submit">Отправить</button>
        </div>
      </div>
    );
  }
}

export default DrawField;
