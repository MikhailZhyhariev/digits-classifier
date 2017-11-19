import React, { Component } from 'react';
import './App.css';

import axios from 'axios';
import Cookies from 'js-cookie';

import DrawField from './DrawField/DrawField'
import ResultTable from './ResultTable/ResultTable'
import Header from './Header/Header'
import AboutApp from './AboutApp/AboutApp'

class App extends Component {
  constructor(props) {
    super(props);

    this.sendData = this.sendData.bind(this);

    this.state = {
      predict: {
        "number": 0,
        "info": [
          {
            type: 'Keras',
            answer: [
              {
                "digit": 0,
                "probability": "100.000%"
              },
              {
                "digit": 1,
                "probability": "100.000%"
              },
              {
                "digit": 2,
                "probability": "100.000%"
              }
            ]
          },
          {
            type: 'Keras',
            answer: [
              {
                "digit": 0,
                "probability": "100.000%"
              },
              {
                "digit": 1,
                "probability": "100.000%"
              },
              {
                "digit": 2,
                "probability": "100.000%"
              }
            ]
          }
        ]
      },
      display: 'none'
    }
  }

  sendData(data) {
    const self = this;

    const csrfToken = Cookies.get('csrftoken');
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios({
      method: 'post',
      url: 'image_add/',
      data: data,
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-type": 'application/x-www-form-urlencoded'
      }
    })
    .then(function (response) {
      console.log(response.data);
      self.setState({
        predict: response.data,
        display: "block"
      })
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  render() {
    const { sendData } = this;
    const { predict, display } = this.state;

    return (
      <div className="App">
        <Header />
        <div className="container">
          <main>
            <DrawField sendData={sendData} />
            <aside>
              <ResultTable data={predict} display={display} />
              <AboutApp />
            </aside>
          </main>
        </div>
      </div>
    );
  }
}

export default App;
