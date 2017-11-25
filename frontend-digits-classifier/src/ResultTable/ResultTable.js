import React, { Component } from 'react';
import './ResultTable.css';


class ResultTable extends Component {
  constructor(props) {
    super(props);

    this.handleNetworkResult = this.handleNetworkResult.bind(this);
  }

  handleNetworkResult(item, key) {
    return (
      <div className="result-table__column" key={key}>
        <div className="result-table__column-part title">{item.type}:</div>
        {item.answer.map( (item, key) =>
          <div className="result-table__column-part">
            <span className="number digit">{item.digit}</span>
            <span className="number">({item.probability})</span>
          </div>
        )}
      </div>
    )
  }

  render() {
    const { data, display } = this.props;
    const { handleNetworkResult } = this;

    return (
      <div className="result-table" style={{display: display}}>
        <div className="result-table__row">
          Результат предсказания:
          <span className="result-table__row-digit">{data.number}</span>
        </div>
        <div className="result-table__row flex">
          {data.info.map( (item, key) =>
            handleNetworkResult(item, key)
          )}
        </div>
      </div>
    );
  }
}

export default ResultTable;
