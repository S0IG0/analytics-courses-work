import {Dispatch, SetStateAction} from "react";

interface Props {
    options: any[],
    setSelected: Dispatch<SetStateAction<any[]>>,
    selected: any[],
}

const SelectedUi = ({options, setSelected, selected}: Props) => {
    return (
        <div className="btn-group">
            <button
                className="btn btn-secondary dropdown-toggle"
                type="button"
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
                aria-expanded="false"
            >
                Выбрать категории
            </button>
            <select
                className="dropdown-menu"
                style={{minHeight: "300px"}}
                multiple
                onChange={event => {
                    setSelected([...event.target.selectedOptions].map(option => option.value))
                }}
                value={selected}
            >
                {options.map((value, index) => (
                    <option key={index} value={index}>{value}</option>
                ))}
            </select>
        </div>
    );
};

export default SelectedUi;