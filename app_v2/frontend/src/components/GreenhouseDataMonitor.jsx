import React from "react";
import axios from "axios";
import { API_URL, GET_DATA_INTERVAL } from "./constants";

/**
 * Данный компонент отображает и обновляет таблицу с 
 * данными по установленному населённому пункту 
 */

class GreenhouseDataMonitor extends React.Component {
    /**
     * Конструктор компонента необходима инициализировать, если в компонент передаются
     * дополнительные параметры или компонент имеет внутренние переменные хранения
     * 
     * @param {*} props - данный аргумент передает атрибуты компонента
     * 
     * this.state - атрибут класса React.Component для хранения внутренних переменных (состояний) компонента
     */
    constructor(props) {
        super(props);
        // устанавливаем состояние компонента по умолчанию
        this.state = {ghdataData: []};
    }

    /**
     * Метод getData отправляет HTTP GET запрос к серверу для получения необходимых данных.
     * 
     * В качестве HTTP-клиента для запросов вместо стандартного fetch импользуется axios.
     * Основные преимущества axios:
     * 
     * - возможность выполнения сразу нескольких HTTP-запросов;
     * - автоматическая конвертация json-данных в объект JS;
     * - поддержка сессий;
     * 
     * Для использования потребуется установка:
     * 
     * npm install axios --save
     * 
     * Подробне об особенностях axios см.: https://blog.logrocket.com/axios-vs-fetch-best-http-requests/
     */
    getData() {
        console.log('GET Request to: ' + API_URL + '/' + this.props.greenhouseName)
        // отправляем запрос на сервер, если данные получены (сервер отвечает в виде массива json-строк), 
        // обновляем массив this.state.ghdataData. В случае ошибки очищаем массив. 
        axios.get(API_URL + '/' + this.props.greenhouseName)
        .then(response => {
            this.setState(state => ({
                ghdataData: response.data,
            }));
        }, error => {
            this.setState(state => ({
                ghdataData: [],
            }));
            console.log(error);
        });
    }

    /**
     * Данный метод динамически рендерит строки таблицы, по данным, 
     * сохраненным в переменной состояния this.state.ghdataData
     */
    renderData() {
        // если массив this.state.ghdataData содержит данные, рендерим строки таблицы
        if (this.state.ghdataData.length > 0) {
            return this.state.ghdataData.map((dataRow) => {
                return(
                    <tr>
                        <td>{this.props.greenhouseName}</td>
                        <td>{dataRow.TemperatureC}</td>
                        <td>{dataRow.CurPressure}</td>
                    </tr>
                );
            });
        }
        // иначе выводим информацию об отсутствии данных
        else {
            return(
                <div className="uk-alert-danger">
                    <a className="uk-alert-close"></a>
                    <p>NO DATA</p>
                </div>
            )
        }
    }
    
    /**
     * Методы componentDidMount() и componentDidUpdate() используются для компонентов,
     * реализованных в виде классов и выполняют дополнительные действия (side effects) при
     * создании и обновлении компонента соответственно.
     * 
     * Для компонентов, реализованных в виде функций, аналогичные действия выполняет 
     * функция (хук) useEffect(). Подробнее см.: https://reactjs.org/docs/hooks-effect.html
     */
     
    /** 
     * Здесь метод componentDidMount() устанавливает внутренний таймер setInterval(), который 
     * выполняет метод getData() каждый 2000 мс.
     * 
     * Использование setInterval() в функциональных компонентах: 
     * https://upmostly.com/tutorials/setinterval-in-react-components-using-hooks
     */
    componentDidMount() {
        this.interval = setInterval(() => this.getData(), GET_DATA_INTERVAL);
    }

    /**
     * Таймер, созданный в компоненте необходимо также очищать при удалении компонента, 
     * для этого используется втроенная функция класса React.Component: componentWillUnmount()
     */
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return(
            <table className="uk-table uk-table-striped">
                <thead>
                    <tr>
                        <th>Greenhouse</th>
                        <th>Temperature &#8451;</th>
                        <th>Pressure</th>
                    </tr>
                </thead>
                <tbody>
                    { this.renderData() }
                </tbody>
            </table>
        );
    }
}

export default GreenhouseDataMonitor;