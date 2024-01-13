/**
 * import './App.css';
 * 
 * Стили по умолчанию App.css и index.css отключены, т.к. в данном приложении 
 * используется пакет со сторонними стилями UIKit (стили с префиксом uk-*).
 * 
 * Стили UIKit подключены через public/index.html:
 * 
 *   <link rel="stylesheet" href="%PUBLIC_URL%/uikit/css/uikit.min.css" />
 *   <script src="%PUBLIC_URL%/uikit/js/uikit.min.js"></script>
 *   <script src="%PUBLIC_URL%/uikit/js/uikit-icons.min.js"></script>
 *
 * Таким же образом можно подключать стили собственной разработки.
 * Подробнее о пакете UIKit см.: https://getuikit.com/docs/installation
 */
import React, { useState } from "react";

import GreenhouseDataMonitor from "./components/GreenhouseDataMonitor";
import GreenhouseDataForm from "./components/GreenhouseDataForm";
import { GREENHOUSE_NAMES } from "./components/constants";

/**
 * Корневой компонент App.js по умолчанию реализован в виде 
 * функционального компонента, для хранения состояния таких 
 * компонентов используется функция (хук) useState().
 * 
 * Зависимые компоненты (GreenhouseDataMonitor и GreenhouseDataForm) 
 * реализованы в виде классов и сохраняют состояние в специальном 
 * атрибуте state. Атрибут greenhouseName={greenhouse} передаёт в данные компоненты
 * значение населённого пункта через объект props и соответствующий атрибут:
 * props.greenhouseName
 * 
 * Подробнее о возможных реализациях React компонентов см.:
 * https://reactjs.org/docs/hooks-state.html
 * 
 */
function App() {
  const [greenhouse, setGreenhouse] = useState('greenhouse1');

  // Рендерим контент.
  // Функция map позволяет рендерить элементы массивов.
  return (
    <div className="uk-section uk-section-muted">
      <div className="uk-margin uk-card uk-card-default uk-card-body uk-text-center">
          <select className="uk-select" value={greenhouse} onChange={(e) => setGreenhouse(e.target.value)}>
            {Object.keys(GREENHOUSE_NAMES).map((greenhouseName) => <option value={greenhouseName}>{greenhouseName}</option>)}
          </select>
      </div>
      <div className="uk-grid uk-text-center">
        <div className="uk-width-expand@m uk-card uk-card-default uk-card-body"><GreenhouseDataForm greenhouseName={greenhouse}/></div>
        <div className="uk-width-expand@m uk-card uk-card-default uk-card-body"><GreenhouseDataMonitor greenhouseName={greenhouse}/></div>
      </div>
    </div>
  );
}

export default App;
