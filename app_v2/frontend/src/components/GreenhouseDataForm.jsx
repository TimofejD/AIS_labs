import React from "react";
import axios from "axios";
import { API_URL, GREENHOUSE_NAMES } from "./constants";

class GreenhouseDataForm extends React.Component {

  constructor(props) {
    super(props);
    // устанавливаем состояние компонента по умолчанию
    this.state = {temperatureC: '', pressure: '', greenhouseId: GREENHOUSE_NAMES[this.props.greenhouseName]};
  }

  /**
   * Обновление данных на сервере (отправка HTTP PUT запроса).
   * 
   * Данная функция вызывается при Submit формы.
   * 
   * Конструкция updateData = (event) => {...} реализует публичную функцию, которую сразу можно
   * привязывать к событиям типа onChange, onSubmit и т.д.
   * 
   * Подробнее об обработчиках событий в компонентах React см.: https://reactjs.org/docs/handling-events.html
   * 
   * @param {*} event 
   */
  updateData = (event) => {
    console.log('POST Request to: ' + API_URL)
    // получаем Id теплицы из словаря и меняем состояние через встроенный метод класса React.Component setState
    this.setState({greenhouseId: GREENHOUSE_NAMES[this.props.greenhouseName]})
    event.preventDefault();   // необходимо, чтобы отключить стандартное поведение формы в браузере (AJAX)
    // формируем данные для отправки на сервер
    let data = {
      Greenhouse_id: this.state.greenhouseId,
      TemperatureC: parseFloat(this.state.TemperatureC),
      CurPressure: parseFloat(this.state.CurPressure),
    };
    // HTTP-клиент axios автоматически преобразует объект data в json-строку
    axios.post(API_URL, data, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
      },
    })
    .then(response => {
      console.log('Response: ' + response.status);
    }, error => {
        console.log(error);
        alert(error);
    });
  }

  render() {
    return (
      <form onSubmit={this.updateData} className="uk-form-stacked">
        <div className="uk-margin">
          <label className="uk-form-label">Temperature:</label>
          <input className="uk-input" type="text" onChange={(e) => {this.setState({TemperatureC: e.target.value})}} />
        </div>
        <div className="uk-margin">
          <label className="uk-form-label">Pressure:</label>
          <input className="uk-input" type="text" onChange={(e) => {this.setState({CurPressure: e.target.value})}} />
        </div>
        <input type="submit" value="Update data" className="uk-button uk-button-primary"/>
      </form>
    );
  }

}

export default GreenhouseDataForm;