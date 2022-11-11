import React from "react";
import {Button, ButtonGroup, Item, ListBox, ListView, Section, View} from "@adobe/react-spectrum";

export function RecentConnections() {
    return (
        <View maxHeight={"400px"} overflow={"auto"}>

            <ButtonGroup align={"start"} orientation="vertical" >
                <Button variant={"negative"}>Jaseci</Button>
                <Button variant={"negative"}>Webble</Button>
                <Button variant={"negative"}>TrueSelph</Button>
                <Button variant={"negative"}>V75 Inc</Button>
                <Button variant={"negative"}>Another project</Button>
                <Button variant={"negative"}>Webble</Button>
                <Button variant={"negative"}>Jaseci</Button>
                <Button variant={"negative"}>TrueSelph</Button>
                <Button variant={"negative"}>V75 Inc</Button>
                <Button variant={"negative"}>GitHub</Button>
            </ButtonGroup>
        </View>

    )
}