import React, { Component } from 'react';
import './DrawField.css';

class DrawField extends Component {
  constructor(props) {
    super(props);

    this.startDraw = this.startDraw.bind(this);
    this.handleDraw = this.handleDraw.bind(this);
    this.clearCanvas = this.clearCanvas.bind(this);
    this.startStopDraw = this.startStopDraw.bind(this);
    this.hintShow = this.hintShow.bind(this);
    this.sendCanvas = this.sendCanvas.bind(this);

    this.state = {
      isDrawing: false,
      startDrawing: false,
      ready: false
    }
  }

  componentDidMount() {
    const ctx = this.refs.field.getContext('2d');
    ctx.fillStyle="white";
    ctx.fillRect(0, 0, 500, 500);
    ctx.fillStyle="black";
    ctx.lineWidth = 20;
  }

  startDraw() {
    const ctx = this.refs.field.getContext('2d');
    const { isDrawing } = this.state;

    if (!isDrawing) {
      ctx.beginPath();

      this.setState({
        startDrawing: true,
        ready: false
      })
    }
  }

  startStopDraw() {
    const ctx = this.refs.field.getContext('2d');

    if (this.isDrawing) {
      ctx.closePath();
    } else {
      ctx.beginPath();
    }

    this.setState({
      isDrawing: !this.state.isDrawing,
      ready: true
    })
  }

  clearCanvas(e) {
    const ctx = this.refs.field.getContext('2d');
    ctx.fillStyle="white";
    ctx.fillRect(0, 0, 500, 500);

    this.setState({
      ready: false,
      isDrawing: false
    })
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

  sendCanvas(e) {
    if (this.state.ready) {
      const base64 = this.refs.field.toDataURL("image/png");
      const image = base64.replace(/^data:image\/(png|jpg);base64,/, "");

      const { sendData } = this.props;
      sendData(image);
    }
  }

  hintShow() {
    const { isDrawing, ready, startDrawing } = this.state;

    if (!isDrawing && !startDrawing && !ready) {
      return <div className="hint" ref="hint">
        <button onClick={this.startDraw} className="start">Нажмите</button>
        <div className="text">чтобы начать</div>
      </div>
    } else if (!isDrawing && startDrawing) {
      return <div className="hint top">
        <div className="text">Кликните левой кнопкой мыши, чтобы начать рисовать</div>
      </div>
    } else {
      return <div className="hint top">
        <div className="text">Кликните левой кнопкой мыши, чтобы закончить</div>
      </div>
    }
  }

  render() {
    const { handleDraw, clearCanvas, startStopDraw, hintShow, sendCanvas } = this;

    return (
      <div className="draw-field">
        {hintShow()}
        <canvas width="500"
                height="500"
                ref="field"
                onMouseMove={handleDraw}
                onClick={startStopDraw} />
        <div className="buttons">
          <button className="button clear"
                  onClick={clearCanvas}>
                  Очистить
          </button>
          <button className="button"
                  onClick={sendCanvas}>
                  Отправить
          </button>
        </div>
      </div>
    );
  }
}

export default DrawField;
