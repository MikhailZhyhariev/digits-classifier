import React, { Component } from 'react';
import './AboutApp.css';

class AboutApp extends Component {
  render() {
    return (
      <div className="about-app">
        <p>Это приложение может распознавать рукописные цифры. Нарисуйте цифру на холсте и нажмите кнопку «Отправить», чтобы увидеть предсказание.</p>
        <p>Нажмите кнопку «Очистить», чтобы очистить холст и снова нарисовать цифру.</p>
        <p>Таблица показывает подробную информацию по всем моделям</p>
      </div>
    );
  }
}

export default AboutApp;
