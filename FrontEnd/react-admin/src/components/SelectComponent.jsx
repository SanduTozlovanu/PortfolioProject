import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import {useState} from "react";
import {useTheme} from "@mui/material";
import {tokens} from "../theme";

export default function SelectComponent({options, defaultLabel, width, onSelect}) {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [selectedOption, setSelectedOption] = useState('');

    const handleChange = (event) => {
        setSelectedOption(event.target.value);
        onSelect(event.target.value);
    };

    return (
        <Box sx={{ minWidth: width, marginLeft: '5px', marginRight: '5px' }}>
            <FormControl fullWidth sx={{
                '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                        borderColor: colors.grey[400],
                    },
                    '&.Mui-focused fieldset': {
                        borderColor: colors.grey[400],
                    },
                },
                '& .MuiInputLabel-outlined.Mui-focused': {
                    color: colors.grey[100],
                }
            }}>
                <InputLabel id="select-label">{defaultLabel}</InputLabel>
                <Select
                    labelId="select-label"
                    id="select"
                    value={selectedOption}
                    label={defaultLabel}
                    onChange={handleChange}
                    MenuProps={{
                        disablePortal: true,
                        keepMounted: true,
                    }}
                >
                    {options.map((option) => (
                        <MenuItem value={option[1]}>{option[0]}</MenuItem>
                        ))}
                </Select>
            </FormControl>
        </Box>
    );
}