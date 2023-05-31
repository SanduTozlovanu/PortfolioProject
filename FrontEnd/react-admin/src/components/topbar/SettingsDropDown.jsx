import React, {useState} from 'react';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    IconButton,
    Menu,
    MenuItem, useTheme
} from '@mui/material';
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import config from "../../config.json";
import axios from "axios";
import {tokens} from "../../theme";
function SettingsDropDown() {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [open, setOpen] = useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
        setOpen(false)
    };
    const resetAccount = async () => {
        try {
            const response = await axios.delete(`${config.url}/user/reset`,
                {
                    headers: {
                        Authorization: JSON.parse(localStorage.getItem("user")).token,
                    }

                });
            window.location.reload();
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div>
            <IconButton
                aria-controls="dropdown-menu"
                aria-haspopup="true"
                onClick={handleClick}
            >
                <SettingsOutlinedIcon />
            </IconButton>
            <Menu
                id="dropdown-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={handleClickOpen}>Reset Account</MenuItem>
            </Menu>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle style={{backgroundColor: colors.primary[400]}}>Confirmation</DialogTitle>
                <DialogContent style={{backgroundColor: colors.primary[400]}}>
                    <DialogContentText>
                        Are you sure that you want to reset the account? All the stocks and transactions will be deleted.
                    </DialogContentText>
                </DialogContent>
                <DialogActions style={{backgroundColor: colors.primary[400]}}>
                    <Button sx={{
                        backgroundColor: colors.redAccent[400],
                        ":hover": {backgroundColor: colors.redAccent[700]}
                    }} onClick={handleClose}>No</Button>
                    <Button sx={{
                        backgroundColor: colors.greenAccent[400],
                        ":hover": {backgroundColor: colors.greenAccent[700]}
                    }} onClick={resetAccount}>Yes</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
export default SettingsDropDown