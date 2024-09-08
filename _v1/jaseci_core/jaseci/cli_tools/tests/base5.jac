import {walker::gen} with 'indirect1.jac';

walker init {
    spawn here walker::gen;
    report -->[0].details['name'];
}