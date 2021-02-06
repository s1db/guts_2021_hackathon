import { useState } from "react";
import cn from "classnames";
import { CrossCircledIcon } from '@radix-ui/react-icons' 

const FilterLabel = ({text, name, handleClick, selected}) => {

  return (
    <div className={cn(
      "rounded-2xl flex text-sm items-center py-2 px-4 mx-1 my-1 transition-colours duration-200 cursor-pointer",
      selected ? "bg-purple-400 text-black hover:bg-purple-200" : "bg-indigo-500 text-white hover:bg-indigo-700"
    )}
    onClick={() => handleClick(name)}
    >
      {text} {selected && (<CrossCircledIcon className="ml-2" />)}
    </div>
  );
};

export default FilterLabel;
