import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import {useState} from "react";

export default function SelectComponent({options, defaultLabel, width, onSelect}) {
    const [selectedOption, setSelectedOption] = useState('');

    const handleChange = (event) => {
        setSelectedOption(event.target.value);
        onSelect(event.target.value);
    };

    return (
        <Box sx={{ minWidth: width, marginLeft: '5px', marginRight: '5px' }}>
            <FormControl fullWidth>
                <InputLabel id="select-label">{defaultLabel}</InputLabel>
                <Select
                    labelId="select-label"
                    id="select"
                    value={selectedOption}
                    label={defaultLabel}
                    onChange={handleChange}
                >
                    {options.map((option) => (
                        <MenuItem value={option}>{option}</MenuItem>
                        ))}
                </Select>
            </FormControl>
        </Box>
    );
}