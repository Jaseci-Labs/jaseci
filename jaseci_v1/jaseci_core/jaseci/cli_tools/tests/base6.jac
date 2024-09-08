import {*} with './logs/indirect1.jac';
import {*} with './main/indirect1.jac';

walker init {
    spawn here walker::gen;
    report -->[0].details['name'];
}